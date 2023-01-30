from django.conf import settings
from django.db import models
from django.utils import timezone
from .backend import VehicleInfo
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField

class Profile(models.Model):
    user = models.OneToOneField(User, null=True, related_name='profile', on_delete=models.CASCADE)
    mobile = PhoneNumberField()
    dob = models.DateTimeField()
    gender = models.IntegerField(choices=[
        (0, 'female'),
        (1, 'male'),
        (2, 'prefer not to tell')
    ])

    def __str__(self):
        return self.user.username

class Group(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    groupNum = models.IntegerField(blank=False, null=False)
    def __str__(self):
        return self.user.first_name + ' ' + self.user.last_name +' '+ '(' + str(self.groupNum) + ')'

class Ride(models.Model):
    # search first if not find create a new one
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    # .add()
    # check if already in the ride
    shared_by_user = models.ManyToManyField(Group, null=True, blank=True)
    vehicle_info = VehicleInfo()
    vehicleType = models.IntegerField(choices=vehicle_info.type, help_text=vehicle_info.description)
    dest = models.TextField(max_length=100)
    arrive_time = models.DateTimeField()
    if_share = models.BooleanField()
    
    # status
    completed = models.BooleanField(default=False)
    confirmed = models.BooleanField(default=False)
    # vehicle
    # drive
    # vehicle
    
    def __str__(self):
        return str(self.pk)

class Vehicle(models.Model):
    vehicle_info = VehicleInfo()
    vehicleType = models.IntegerField(choices=vehicle_info.type, help_text=vehicle_info.description)
    owner = models.OneToOneField(User, on_delete=models.CASCADE, related_name='vehicle', default=None)
    plateNumber = models.CharField(max_length=20)


        