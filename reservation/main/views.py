from django.shortcuts import render, get_object_or_404
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework import viewsets
from rest_framework.views import APIView
from .models import  *
from .serializers import *
from rest_framework.response import Response
from django.conf import settings
from django.http import HttpResponse
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
import stripe

class MovieViewSet(viewsets.ModelViewSet):
    permission_classes = [AllowAny]
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer

class ShowTimeViewset(viewsets.ModelViewSet):
    Permission_classes = [AllowAny]
    queryset = ShowTime.objects.all()
    serializer_class = ShowTimeSerializer

# get showtime for specific movie
class ShowTimeMovie(APIView):
    permission_classes = [AllowAny]
    def get(self, request, movie_id):
        if not movie_id:
            return Response({'error': 'Movie ID is required'}, status=status.HTTP_400_BAD_REQUEST)
        movie = get_object_or_404(Movie, id=movie_id)
        show_time = get_object_or_404(ShowTime, movie=movie)
        serializer = ShowTimeSerializer(show_time)
        return Response(serializer.data, status=status.HTTP_200_OK)

class SeatViewSet(viewsets.ModelViewSet):
    permission_classes = [AllowAny]
    queryset = Seat.objects.all()
    serializer_class = SeatSerializer

class ReservationView(APIView):
    permission_classes = [IsAuthenticated]
    # cancel a reservation
    def delete(self, reservation_id):
        if not reservation_id:
            return Response({'error': 'Reservation ID is required'}, status=status.HTTP_400_BAD_REQUEST)
        reservation = get_object_or_404(Reservation, id=reservation_id)
        reservation.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    # get reservation details
    def get(self, request, reservation_id):
        if not reservation_id:
            return Response({'error': 'Reservation ID is required'}, status=status.HTTP_400_BAD_REQUEST)
        reservation = get_object_or_404(Reservation, id=reservation_id)
        serializer = ReservationSerializer(reservation)
        return Response(serializer.data, status=status.HTTP_200_OK)
    # list user reservations
    def get(self, request):
        user = request.user
        reservation = get_object_or_404(Reservation, user=user)
        serializer = ReservationSerializer(reservation)
        return Response(serializer.data, status=status.HTTP_200_OK)
    # create a reservation endpoint
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

# to display the list of seats who is available in a specific show-time
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

stripe.api_key = settings.STRIPE_SECRET_KEY
class CreateCheckoutSessionView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request,reservation_id):
        reservation = get_object_or_404(Reservation, id=reservation_id)
        try:
            checkout_session = stripe.checkout.Session.create(
                payment_method_types=["card"],
                metadata={
                    'reservation_id' : str(reservation_id),
                    'user_email' : reservation.user.email
                },
                mode='payment',
                success_url='http://localhost:8000/payment/success/',
                cancel_url='http://localhost:8000/payment/cancel/',
                line_items=[
                    {
                        'price_data': {
                            'currency': 'usd',
                            'product_data': {
                                'name': f'Seat Reservation for ShowTime {reservation.show_time.id}',
                            },
                            'unit_amount': int(reservation.price * 100),  # in cents
                        },
                        'quantity': 1,
                    },
                ],
            )

            return Response({'checkout_url': checkout_session.url})

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

def payment_success(request):
    return HttpResponse('payment completed successfully! ✅')

def payment_cancel(request):
    return HttpResponse('payment  Canceled ❎')
@method_decorator(csrf_exempt, name='dispatch')
class StripeWebhookView(APIView):
    def post(self, request):
        payload = request.body
        sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')
        endpoint_secret = settings.STRIPE_WEBHOOK_SECRET
        try:
            event = stripe.Webhook.construct_event(
                payload, sig_header, endpoint_secret
            )
        except ValueError as e:
            return HttpResponse(status=400)
        except stripe.error.SignatureVerificationError as e:
            return HttpResponse(status=400)

        session = event['data']['object']
        if event['type'] == 'checkout.session.completed':
            reservation_id = session['metadata']['reservation_id']
            user_email = session['metadata']['user_email']
            product = Reservation.objects.filter(id=reservation_id).first()
            user = User.objects.get(email=user_email)
            PurchaseHistory.objects.create(reservation=product, is_succeeded=True, user=user)
            reservation = get_object_or_404(Reservation, user=user)
            reservation.is_paid = True
            reservation.save()

        elif event['type'] == 'checkout.session.async_payment_failed':
            product_id = session['metadata']['product_id']
            user_email = session['metadata']['user_email']
            product = Reservation.objects.get(id=product_id)
            user = User.objects.get(email=user_email)
            PurchaseHistory.objects.create(reservation=product, is_succeeded=False, user=user)

        return HttpResponse(status=200)

class PaymentStatusView(APIView):
    def get(self, request, reservation_id):
        if not reservation_id:
            return Response({'error': 'Reservation ID is required'}, status=status.HTTP_400_BAD_REQUEST)
        payment = get_object_or_404(PurchaseHistory, reservation=reservation_id)
        serializer = PurchaseHistorySerializer(payment)
        return Response(serializer.data, status=status.HTTP_200_OK)

