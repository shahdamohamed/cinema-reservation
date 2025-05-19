from django.shortcuts import render
from rest_framework import viewsets
from .models import  *
from .serializers import *
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from django.conf import settings
from django.http import JsonResponse
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny


# to display the list of movies and their details
class MovieViewSet(viewsets.ModelViewSet):
    permission_classes = [AllowAny]
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer

# to do a reservation for specific show time and seat and check if the seat is already reserved for that show time
class ReservationViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer

    def perform_create(self, serializer):
        seat = serializer.validated_data['seat']
        show_time = serializer.validated_data['show_time']
        if Reservation.objects.filter(seat=seat, show_time=show_time).exists():
            raise ValidationError('This seat is already reserved for this show time.')
        serializer.save(user=self.request.user)

# to display the list of seats in a specific cinema hall and check if the seat is available or not
class CinemaHallViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = CinemaHall.objects.all()
    serializer_class = CinemaHallSerialzer

    @action(detail=True, methods=['get'])
    def available_seats(self, request, Pk=None):
        hall = self.get.abject()
        show_time_id = request.query_params.get('show_time')

        if not show_time_id:
            return Response({'error':'show_time is required parameter'}, status=400)
        try:
            show_time = ShowTime.objects.get(id=show_time_id)
        except:
            return Response({'error':'show_time not found'}, status=404)
        reserved_seats_id = Reservation.objects.filter(show_time=show_time, status='Confirmed').values_list('seat', flat=True)
        available_seats = Seat.objects.filter(hall=hall).exclude(id__in=reserved_seats_id)
        serializer = SeatSerializer(available_seats, many=True)
        return Response(serializer.data)

# to display show times
class ShowTimeViewset(viewsets.ModelViewSet):
    Permission_classes = [AllowAny]
    queryset = ShowTime.objects.all()
    serializer_class = ShowTimeSerializer   
