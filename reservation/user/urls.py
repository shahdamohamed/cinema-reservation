from django.urls import path
from .views import * 
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenBlacklistView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('resend-otp/', ResendOTPView.as_view(), name='resend_otp'),
    path('verify-account-otp/', OTPVerifyAccountView.as_view(), name='verify-account_otp'),
    path('forget-password/', ForgetPasswordView.as_view(), name='send-otp-for-change-pass'),
    path('verify-reset-password-otp/',OTPVerifyResetPassView.as_view(), name='verify_reset_password-otp'),
    path('reset-password/', ResetPasswordView.as_view(), name='reset-password'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/logout/', TokenBlacklistView.as_view(), name='token_blacklist'),

]
