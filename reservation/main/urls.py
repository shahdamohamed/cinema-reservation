# main/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register('movies', views.MovieViewSet)
router.register('cinema_halls', views.CinemaHallViewSet)
router.register('show_times', views.ShowTimeViewset)
router.register('reservations', views.RservationViewSet)
router.register('seats', views.SeatViewSet)
router.register('users', views.UserViewSet)
router.register('payments', views.PaymentViewSet)
urlpatterns = [
    path('', include(router.urls)), 
]
