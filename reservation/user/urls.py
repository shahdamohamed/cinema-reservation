from django.urls import path
from .views import * 
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenBlacklistView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('generate_otp/', GenerateOTP.as_view(), name='generate-otp'),
    path('verify_otp/', VarifyOTP.as_view(), name='verify-otp'),
    path('reset_password/', ResetPasswordView.as_view(), name='reset-password'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/logout/', TokenBlacklistView.as_view(), name='token_blacklist'),
]
