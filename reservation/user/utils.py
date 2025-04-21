from django.core.mail import send_mail
import random
from .models import *

def generate_otp():
    return str(random.randint(100000, 999999))

def send_otp_mail(user):
    code = generate_otp()
    OTP.objects.create(user=user, code=code)
    send_mail(
        subject='Your OTP Code',
        message=f'Your OTP code is {code}',
        from_email='noreply@example.com',
        recipient_list=[user.email],
        fail_silently=False,
    )
