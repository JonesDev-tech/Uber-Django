from django.conf import settings
from django.db import models
from django.utils import timezone
from .backend import VehicleInfo


class Ride(models.Model):
    # search first if not find create a new one
    owner = models.ForeignKey(Passenger, on_delete=models.CASCADE)
    # .add()
    # check if already in the ride
    shared_by = models.ManyToManyField(Passenger)
    vehicleType = models.IntegerField()
    dest = models.TextField(max_length=100)
    arrive_time = models.DateTimeField()
    if_share = models.BooleanField()
    
    # status
    completed = models.BooleanField(default=False)
    confirmed = models.BooleanField(default=True)
    # vehicle
    
    def __str__(self):
        return self.pk


class Passenger(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    groupNum = models.IntegerField(blank=False, null=False)
    
class Vehicle(models.Model):



        