# main/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *
from . import views

router = DefaultRouter()
router.register('movies', views.MovieViewSet)
router.register('show_times', views.ShowTimeViewset)
router.register('seats', views.SeatViewSet)
# router.register('payments', views.PaymentViewSet)
urlpatterns = [
    path('', include(router.urls)),
    path('reservation/', ReservationView.as_view(), name='reservation'),
    path('available-seats/', views.SeatsInHallView.as_view(), name='available-seats'),
]
