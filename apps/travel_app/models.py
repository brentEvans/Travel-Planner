from django.db import models
import bcrypt
from datetime import date, datetime

# Create your models here.

class UserManager(models.Manager):
    def registration_validator(self, postData):
        errors = {}
        if len(User.objects.filter(username=postData['username'])) > 0:
            errors['matching_user'] = 'There is already an account associated with this email address.  Please log in!'
        if len(postData['name']) < 3:
            errors['name'] = 'Name must be at least 3 characters long!'
        if len(postData['username']) < 3:
            errors['username'] = 'Username must be at least 3 characters long!'
        if len(postData['password']) < 8:
            errors['password'] = 'Password must be at least 8 characters!'
        if postData['password'] != postData['confirm_pw']:
            errors['confirm_pw'] = 'Password and password confirmation must match!'
        return errors
    def login_validator(self, postData):
        errors = {}
        matching_user = User.objects.filter(username=postData['username'])
        if len(matching_user) < 1:
            errors['matching_user'] = 'There is no account associated with your username.  Please register!'
        else:
            user = matching_user[0]
            if bcrypt.checkpw(postData['password'].encode(), user.password.encode()):
                print('password match')
            else:
                print('failed password')
                errors['failed_password'] = 'You entered the wrong password.  Please try again.'
        return errors

class TripManager(models.Manager):
    def plan_validator(self, postData):
        errors = {}
        if len(postData['destination']) < 1:
            errors['destination'] = 'Destination cannot be blank!'
        if len(postData['plan']) < 1:
            errors['plan'] = 'Description cannot be blank!'
        now = datetime.now()
        start_date = postData['travel_start_date']
        end_date = postData['travel_end_date']
        if start_date < str(now) or end_date < str(now):
            errors['dates_in_past'] = 'Your trip dates must be in the future!'
        if end_date < start_date:
            errors['dates'] = 'The end of your trip cannot be prior to the start of your trip!'
        return errors

class User(models.Model):
    name = models.CharField(max_length=255)
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

class Trip(models.Model):
    destination = models.CharField(max_length=100)
    travel_start_date = models.DateField()
    travel_end_date = models.DateField()
    plan = models.TextField()
    planned_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='trips_planned')
    users_on_trip = models.ManyToManyField(User, related_name='trips_joining')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = TripManager()
