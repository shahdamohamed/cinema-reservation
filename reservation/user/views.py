from rest_framework import generics
from .serializers import *
from django.contrib.auth import get_user_model
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.conf import settings
from .models import *

User = get_user_model()

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer

class OTPVerifyView(generics.GenericAPIView):
    serializer_class = OTPVerifySerializer
    
    def post(self, request):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            email = serializer.validated_data['email']
            code = serializer.validated_data['code']

            try:
                user = User.objects.get(email=email)
                otp = OTP.objects.filter(user=user, code=code).last()

                if otp and not otp.is_expired():
                    user.is_active = True
                    user.save()
                    otp.delete()
                    return Response({'message': 'تم التحقق بنجاح ✅'}, status=200)
                else:
                    return Response({'error': 'OTP غير صحيح أو منتهي'}, status=400)
            except User.DoesNotExist:
                return Response({'error': 'email not found'}, status=400)
        return Response(serializer.errors, status=400)
    

class LogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        


class SendTestEmailView(APIView):
    def get(self, request):
        send_mail(
            subject=' test email',
            message='test email',
            from_email='noreply@example.com',
            recipient_list=['test@example.com'],  
            fail_silently=False,
        )
        return Response({'message': 'Email sent successfully' })

class PasswordResetRequestView(APIView):
    def post(self, request):
        serializer = PasswordResetRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data['email']
        user = User.objects.get(email=email)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = PasswordResetTokenGenerator().make_token(user)

        reset_url = f"http://frontend-app.com/reset-password?uid={uid}&token={token}"
        send_mail(
                'reset your password',
                f"click the link to reset your password {reset_url}",
                settings.EMAIL_HOST_USER,
                [email],
                fail_silently=False,
            )
        return Response({'message': 'if this email is registered, you will recieve a password reset link '})

class PasswordResetConfirmView(APIView):
    def post(self, request):
        serializer = PasswordResetConfirmSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        uidb64 = serializer.validated_data('uid')
        token = serializer.validated_data('token')
        new_password = serializer.validated_data('new_password')

        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, get_user_model().DoesNotExist):
            return Response({'error': 'Invalid uid'}, status=status.HTTP_400_BAD_REQUEST)
        
        if PasswordResetTokenGenerator().check_token(user, token):
            user.set_password(new_password)
            user.save()
            return Response({'message': 'Password reset successful'}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid or expired token'}, status=status.HTTP_400_BAD_REQUEST)
