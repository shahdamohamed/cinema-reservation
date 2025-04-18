from rest_framework import generics
from .serializers import RegisterSerializer
from django.contrib.auth import get_user_model
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.mail import send_mail


User = get_user_model()

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    
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
            recipient_list=['test@example.com'],  # أي إيميل تحطيه هنا
            fail_silently=False,
        )
        return Response({'message': 'Email sent successfully' })