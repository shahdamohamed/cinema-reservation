from django.contrib import admin
from .models import User, OTPModel

admin.site.register(OTPModel)
admin.site.register(User)