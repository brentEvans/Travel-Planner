from django.db import models
import bcrypt
from datetime import date, datetime

# TODO
    # Users can also post messages to other users and comment on each trip.  


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

class CommentManager(models.Manager):
    def comment_validator(self, postData, this_trip, this_user, users_on_trip):
        errors = {}
        if not this_user in users_on_trip:
            errors['user'] = 'You must join the trip before posting comments!'
        if len(postData['body']) < 1:
            errors['body'] = 'Comments cannot be blank!'
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

class Comment(models.Model):
    body = models.TextField(max_length=1000)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE, related_name='comments')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = CommentManager()

# Manager class for comments
    # only people who've joined the trip may leave comments
    # allow trip planner to remove comments
        # and remove people...



# TODO 
    # send messages between users