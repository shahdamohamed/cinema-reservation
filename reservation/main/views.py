from django.shortcuts import render
from rest_framework import viewsets
from .models import  *
from .serializers import *
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from rest_framework.views import APIView
from rest_framework import status


# to display the list of movies and their details
class MovieViewSet(viewsets.ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer

# to do a reservation for specific show time and seat and check if the seat is already reserved for that show time
class ReservationViewSet(viewsets.ModelViewSet):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer

    def perform_create(self, serializer):
        seat = serializer.validated_data['seat']
        show_time = serializer.validated_data['show_time']
        raise ValidationError('This seat is already reserved for this show time.')
        serializer.save(user=self.request.user)

# to display the list of seats in a specific cinema hall and check if the seat is available or not
class CinemaHallViewSet(viewsets.ModelViewSet):
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
    queryset = ShowTime.objects.all()
    serializer_class = ShowTimeSerializer   

class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer

class SignUpView(APIView):
    def post(self, request):
        serializer = SignUpSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            return Response(serializer.validated_data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class LogoutView(APIView):
    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()  # delete this token
            return Response({"message": "Successfully logged out."}, status=200)
        except KeyError:
            return Response({"error": "Please provide a valid refresh token."}, status=400)

