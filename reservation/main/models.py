from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from user.models import User

class Movie(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    duration = models.DurationField(blank=True, null=True)
    rating = models.FloatField(blank=True, null=True)
    language = models.CharField(max_length=100, blank=True, null=True)
    movie_picture = models.ImageField(upload_to='movie_pictures/', blank=True, null=True)
    
    def __str__(self):
        return self.title

class CinemaHall(models.Model):
    hall_number = models.IntegerField(unique=True)
    seats_amount = models.IntegerField(default=60)
    def __str__(self):
        return f'hall {self.hall_number}'

class Seat(models.Model):
    hall = models.ForeignKey(CinemaHall, on_delete=models.CASCADE, related_name='seats')
    seat_number = models.IntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(60)
        ]
    )
    seat_type_choices = [
        ('Standard', 'Standard'),
        ('VIP', 'VIP'),
    ]
    seat_type = models.CharField(choices=seat_type_choices, default='Standard')
    def __str__(self):
        return f"seat {self.seat_number} in hall {self.hall.hall_number}"

class ShowTime(models.Model):
    seat = models.ManyToManyField(Seat, related_name='show_times')
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='show_times')
    hall = models.ForeignKey(CinemaHall, on_delete=models.CASCADE, related_name='show_times')
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    price = models.FloatField(default=125.0)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f'{self.movie} - {self.start_time} - {self.hall}'

class Reservation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reservations')
    show_time = models.ForeignKey(ShowTime, on_delete=models.CASCADE, related_name='reservations')
    seat = models.ManyToManyField(Seat, related_name='reservations')
    created_at = models.DateTimeField(auto_now_add=True)
    is_paid = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    price = models.FloatField(default=125)
    def __str__(self):
        return f"{self.user.username}"

class PurchaseHistory(models.Model):
    reservation = models.ForeignKey(Reservation, on_delete=models.CASCADE, related_name='purchase_history')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='purchase_history')
    is_succeeded = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username
