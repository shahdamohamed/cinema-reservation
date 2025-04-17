from django.contrib import admin
from .models import *

admin.site.register(Movie)
admin.site.register(CinemaHall)
admin.site.register(Seat)
admin.site.register(ShowTime)
admin.site.register(Reservation)
