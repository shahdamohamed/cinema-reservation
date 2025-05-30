from logging import exception
from django.db.migrations import serializer
from django.shortcuts import render, get_object_or_404
from rest_framework import viewsets
from rest_framework.views import APIView
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

# to display show times
class ShowTimeViewset(viewsets.ModelViewSet):
    Permission_classes = [AllowAny]
    queryset = ShowTime.objects.all()
    serializer_class = ShowTimeSerializer

class SeatViewSet(viewsets.ModelViewSet):
    permission_classes = [AllowAny]
    queryset = Seat.objects.all()
    serializer_class = SeatSerializer
# create a reservation endpoint
class ReservationView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = self.request.user
        show_time_id = request.data.get('showtime')
        seat_ids = request.data.get('seat')

        # fetch data from request body
        show_time = get_object_or_404(ShowTime, id = show_time_id)
        seats = []
        total_price = 0
        for seat_id in seat_ids:
            seat = get_object_or_404(Seat, id = seat_id)

            # make sure this seat is available
            if Reservation.objects.filter(show_time=show_time, seat=seat).exists():
                return Response({"error": "This seat is already reserved for the selected show time."}, status=400)

            # calculate the price of the seat based on the seat type
            if seat.seat_type == 'Standard':
                price = show_time.price
            else:
                price = show_time.price + 60

            seats.append(seat) # add the seat to seats array
            total_price += price # add price od=f that seat to the total price

        # create a reservation
        reservation = Reservation.objects.create(
            user=user,
            show_time=show_time,
            price=total_price
        )
        reservation.seat.set(seats)
        serializer = ReservationSerializer(reservation)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

# to display the list of seats who is available in a specific show time
class SeatsInHallView(APIView):
    permission_classes = [AllowAny]
    def get(self, request, *args, **kwargs):
        show_time_id = request.data.get('showtime')
        show_time = get_object_or_404(ShowTime, id = show_time_id)
        # get all seats
        seats = show_time.seat.all()
        available_seats = []
        unavailable_seats = []
        for seat in seats :
            if Reservation.objects.filter(show_time=show_time, seat=seat).exists():
                unavailable_seats.append(seat)
            else:
                available_seats.append(seat)
        serializer = SeatSerializer(available_seats, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)



