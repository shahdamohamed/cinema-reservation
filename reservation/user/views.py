from rest_framework import generics
from rest_framework.generics import get_object_or_404
from .serializers import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from .models import User
from .utils import *

class GenerateOTP(APIView):
    permission_classes = (AllowAny,)
    def post(self, request):
        serializer = OTPGenerateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']
        user = get_object_or_404(User, email=email)
        if OTPModel.objects.filter(user=user) :
            OTPModel.objects.filter(user=user).delete()
        send_otp_mail(user)
        return Response({'message': 'OTP Sent Successfully'})

class VarifyOTP(APIView):
    permission_classes = (AllowAny,)
    def post(self, request):
        serializer = OTPVerifySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']
        code = serializer.validated_data['code']
        user = get_object_or_404(User, email=email)
        otp = get_object_or_404(OTPModel, user=user, code=code)
        if not otp:
            return Response({'message': 'OTP Not Found'}, status=status.HTTP_404_NOT_FOUND)
        if otp:
            if user.is_active:
                otp.is_valid = True
                otp.save()
                return Response({'message': 'OTP verified successfully'}, status=status.HTTP_200_OK)
            if not user.is_active:
                user.is_active = True
                user.save()
                otp.delete()
                return Response({'message': 'Your email is active now'}, status=status.HTTP_200_OK)


class RegisterView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        serializerr = UserSerializer(data=request.data)
        serializerr.is_valid(raise_exception=True)
        username = serializerr.validated_data['username']
        first_name = serializerr.validated_data['first_name']
        last_name = serializerr.validated_data['last_name']
        email = serializerr.validated_data['email']
        password = serializerr.validated_data['password']
        phone = serializerr.validated_data['phone']
        user = User.objects.create_user(username=username,first_name=first_name,last_name=last_name,email=email,password=password,phone=phone)
        user.is_active = False
        user.save()
        send_otp_mail(user)
        return Response(serializerr.data, status=status.HTTP_200_OK)
    def get(self, request, user_id):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user_id']
        get_object_or_404(User, id=user_id)
        return Response(serializer.data, status=status.HTTP_200_OK)

# change password after verification
class ResetPasswordView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = ResetPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']
        new_password = serializer.validated_data['new_password']
        user = get_object_or_404(User, email=email)
        otp = OTPModel.objects.filter(user=user, is_valid=True)
        if not otp:
            return Response({'error': 'Invalid OTP'}, status=status.HTTP_404_NOT_FOUND)
        user.set_password(new_password)
        user.save()
        otp.delete()
        return Response({'message': 'password reset successfully'}, status=status.HTTP_200_OK)












