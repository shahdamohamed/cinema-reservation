# main/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *
from . import views

router = DefaultRouter()
router.register('movies', views.MovieViewSet)
router.register('cinema_halls', views.CinemaHallViewSet)
router.register('show_times', views.ShowTimeViewset)
router.register('reservations', views.ReservationViewSet)
router.register('payments', views.PaymentViewSet)
urlpatterns = [
    path('', include(router.urls)), 
     path('signup/', SignUpView.as_view(), name='signup'),
      path('login/', LoginView.as_view(), name='login'),
       path('logout/', LogoutView.as_view(), name='logout'),
]
