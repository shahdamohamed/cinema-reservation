from rest_framework import serializers
from .utils import send_otp_mail
from .models import User

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name',  'email', 'password', 'phone']

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            email=validated_data['email'],
            password=validated_data['password'],
            phone=validated_data['phone'],
        )
        user.is_active = False
        user.save()
        send_otp_mail(user)
        return user

class ResendOTPSerializer(serializers.Serializer):
    email = serializers.EmailField()
    
class OTPVerifySerializer(serializers.Serializer):
    email = serializers.EmailField()
    code = serializers.CharField(max_length=6)

class ForgetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()

class ResetPasswordSerialzer(serializers.Serializer):
    email = serializers.EmailField()
    new_password = serializers.CharField(write_only=True)