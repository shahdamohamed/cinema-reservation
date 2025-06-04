from rest_framework import serializers
from .models import Movie, ShowTime, Reservation, Seat, CinemaHall, PurchaseHistory

class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = '__all__'

class ShowTimeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShowTime
        fields = '__all__'

class SeatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Seat
        fields = '__all__'

class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = '__all__'

class CinemaHallSerialzer(serializers.ModelSerializer):
    class Meta:
        model = CinemaHall
        fields = '__all__'

class PurchaseHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = PurchaseHistory
        fields = '__all__'
