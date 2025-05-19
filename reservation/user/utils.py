from django.core.mail import send_mail
import random
from .models import *
from django.conf import settings

def generate_otp():
    return str(random.randint(100000, 999999))

def send_otp_mail(user):
    code = generate_otp()
    OTPModel.objects.create(user=user, code=code)
    send_mail(
        subject='Your OTP Code',
        message=f'Your OTP code is {code}',
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[user.email],
        fail_silently=False,
    )

def send_reset_password_mail(user):
    code = generate_otp()
    OTPModel.objects.create(user=user, code=code)
    send_mail(
        subject='Reset your Password OTP',
        message=f'your OTP is {code}',
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[user.email],
        fail_silently=False,
    )