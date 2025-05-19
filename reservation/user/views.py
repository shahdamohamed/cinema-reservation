import datetime
from rest_framework import generics
from rest_framework.generics import get_object_or_404
from .serializers import *
from django.contrib.auth import get_user_model
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.conf import settings
from .models import *
from .utils import *

User = get_user_model()

class RegisterView(generics.CreateAPIView):
    permission_classes = [AllowAny]
    queryset = User.objects.all()
    serializer_class = RegisterSerializer

# for verify the account
class OTPVerifyAccountView(APIView):
    serializer_class = OTPVerifySerializer
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']
        code = serializer.validated_data['code']
        user = get_object_or_404(User, email=email)
        otp = OTPModel.objects.filter(user=user, code=code).last()
        if not otp:
            return Response({'error': 'Invalid code'}, status=status.HTTP_400_BAD_REQUEST)
        if otp:
            user.is_active = True
            user.save()
            otp.delete()
            return Response({'message': 'OTP verified successfully'}, status=status.HTTP_200_OK)

# verify the OTP for reset password
class OTPVerifyResetPassView(generics.GenericAPIView):
    serializer_class = OTPVerifySerializer
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']
        otp = serializer.validated_data['code']
        user = get_object_or_404(User, email=email)
        otp_obj = OTPModel.objects.filter(user=user, code=otp, is_valid=False).last()
        if not otp_obj:
            return Response({'error': 'Invalid OTP'}, status=status.HTTP_404_NOT_FOUND)
        otp_obj.is_valid = True
        otp_obj.save()
        return Response({'message': 'OTP verified successfully'})

# sent OTP to the email
class ForgetPasswordView(APIView):
    permission_classes = [AllowAny]
    serializer_class = ForgetPasswordSerializer
    def post(self, request, *args, **kwargs):
            serializer = self.serializer_class(data=request.data)
            serializer.is_valid(raise_exception=True)
            user = get_object_or_404(User, email=serializer.validated_data['email'])
            send_otp_mail(user)
            return Response({'message': 'OTP sent Successfully to the email.'}, status=status.HTTP_200_OK)

class ResendOTPView(APIView):
    permissions_classes = [AllowAny]
    serializer = ResendOTPSerializer
    def post(self, request, *args, **kwargs):
        serializer = self.serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = get_object_or_404(User, email=serializer.validated_data['email'])
        OTPModel.objects.filter(user=user).delete()
        send_otp_mail(user)
        return Response({'message': 'OTP Resent Successfully'})

# change password after verification
class ResetPasswordView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = ResetPasswordSerialzer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']
        new_password = serializer.validated_data['new_password']
        user = get_object_or_404(User, email=email)
        otp_obj = OTPModel.objects.filter(user=user, is_valid=True).last()
        if not otp_obj:
            return Response({'error': 'Invalid OTP'}, status=status.HTTP_404_NOT_FOUND)
        user.set_password(new_password)
        user.save()
        OTPModel.objects.filter(user=user, code=otp_obj.code).delete()
        return Response({'message': 'password reset successfully'}, status=status.HTTP_200_OK)












