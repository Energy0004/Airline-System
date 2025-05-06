from django.contrib.auth.models import AbstractUser, Group, Permission, User
from django.db import models

class Airport(models.Model):
    code = models.CharField(max_length=3)
    city_name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.city_name} ({self.code})"

class Flight(models.Model):
    origin = models.ForeignKey(Airport, on_delete=models.CASCADE, related_name='departures')
    destination = models.ForeignKey(Airport, on_delete=models.CASCADE, related_name='arrivals')
    duration = models.IntegerField()
    capacity = models.IntegerField()
    def __str__(self):
        return f'{self.origin} to {self.destination}, {self.duration}, {self.capacity}'

class Passenger(models.Model):
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    def __str__(self):
        return f'{self.name}, {self.email}'

class Booking(models.Model):
    passenger = models.ForeignKey(Passenger, on_delete=models.CASCADE, related_name='passengers')
    flight = models.ForeignKey(Flight, on_delete=models.CASCADE, related_name='flights')
    booking_code = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    def __str__(self):
        return f'{self.passenger}, {self.flight}, {self.booking_code}'