from rest_framework import serializers
from .models import Movie, ShowTime, Reservation, Seat, User, CinemaHall, Payment
from rest_framework_simplejwt.tokens import RefreshToken

class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = '__all__'

class ShowTimeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShowTime
        fields = '__all__'

class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = '__all__'

class SeatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Seat
        fields = '__all__'

class SignUpSerializer(serializers.ModelSerializer):
    pass
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'phone']

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            phone=validated_data['phone']
        )
        return user
    
    class LoginSerializer(serializers.Serializer):
        username = serializers.CharField()
        password = serializers.CharField()

        def validate(self, data):
            user = User.objects.filter(username=data['username']).first()
            if user is None or not user.check_password(data['password']):
                raise serializers.ValidationError("Invalid username or password")
            
            refresh = RefreshToken.for_user(user)
            return {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }

class CinemaHallSerialzer(serializers.ModelSerializer):
    class Meta:
        model = CinemaHall
        fields = '__all__'

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'
