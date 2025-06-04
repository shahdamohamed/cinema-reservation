from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register('movies', views.MovieViewSet)
router.register('show_times', views.ShowTimeViewset)
router.register('seats', views.SeatViewSet)
urlpatterns = [
    path('', include(router.urls)),
    path('showtime/<int:movie_id>', views.ShowTimeMovie.as_view(), name='show times by movie'),
    path('reservation/', views.ReservationView.as_view(), name='reservation'),
    path('available-seats/', views.SeatsInHallView.as_view(), name='available-seats'),
    path('create-checkout-session/<int:reservation_id>/', views.CreateCheckoutSessionView.as_view(), name='create-checkout-session'),
    path('payment/success/', views.payment_success, name='payment-success'),
    path('payment/cancel/', views.payment_cancel, name='payment-cancel'),
    path('webhook/', views.StripeWebhookView.as_view(), name='stripe-webhook'),
    path('payment-status/<int:reservation_id>', views.PaymentStatusView.as_view(), name='payment-status'),
]
