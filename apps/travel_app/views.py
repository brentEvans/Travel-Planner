from django.shortcuts import render, redirect
from .models import *
from django.contrib import messages
import bcrypt

def index(request):
    return render(request, 'travel_app/index.html')

def validate_registration(request):
    errors = User.objects.registration_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    else:
        hash1 = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
        this_user = User.objects.create(name=request.POST['name'], username=request.POST['username'], password=hash1.decode())
        request.session['logged_in_user_id'] = this_user.id 
        print("*"*100)
        print(this_user.id) 
        print("*"*100)
        request.session['logged_in_user_name'] = this_user.name
        request.session['logged_in_user_username'] = this_user.username
        return redirect('/travels')

def validate_login(request):
    errors = User.objects.login_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    else: 
        this_user = User.objects.get(username=request.POST['username'])
        request.session['logged_in_user_id'] = this_user.id 
        request.session['logged_in_user_name'] = this_user.name
        request.session['logged_in_user_username'] = this_user.username
        return redirect('/travels')

def travels(request):
    # TODO
        # figure out what Test User's id is on deployed site and update!

    print("*"*100)
    print(request.session['logged_in_user_id']) 
    print("*"*100)

    try:
        request.session['logged_in_user_id']
    except KeyError:
        this_user = User.objects.get(id=3)                # change id to match deployed Test User object id
        request.session['logged_in_user_id'] = this_user.id
        request.session['logged_in_user_name'] = this_user.name
        request.session['logged_in_user_username'] = this_user.username
        context = {
            'this_user_trips': Trip.objects.filter(users_on_trip=this_user.id),       # change id to match deployed Test User object id
            'all_trips_ex_user': Trip.objects.exclude(users_on_trip=this_user.id),       # change id to match deployed Test User object id
        }
    else:
        this_user = User.objects.get(id=request.session['logged_in_user_id']) 
        context = {
            'this_user_trips': Trip.objects.filter(users_on_trip=this_user.id),
            'all_trips_ex_user': Trip.objects.exclude(users_on_trip=this_user.id),
        }

    # if (not request.session['logged_in_user_id'] ):
    #     this_user = User.objects.get(id=12)                # change id to match deployed Test User object id
    #     request.session['logged_in_user_id'] = this_user.id
    #     request.session['logged_in_user_name'] = this_user.name
    #     request.session['logged_in_user_username'] = this_user.username
    #     context = {
    #         'this_user_trips': Trip.objects.filter(users_on_trip=12),       # change id to match deployed Test User object id
    #         'all_trips_ex_user': Trip.objects.exclude(users_on_trip=12),       # change id to match deployed Test User object id
    #     }
    # else:
    #     this_user = User.objects.get(id=request.session['logged_in_user_id']) 
    #     context = {
    #         'this_user_trips': Trip.objects.filter(users_on_trip=this_user.id),
    #         'all_trips_ex_user': Trip.objects.exclude(users_on_trip=this_user.id),
    #     }
    # print('*'*100)
    # print(this_user_trips)
    return render(request, 'travel_app/user_page.html', context)









def join_trip(request, number):
    this_user = User.objects.get(id=request.session['logged_in_user_id'])
    this_trip = Trip.objects.get(id=number)
    this_trip.users_on_trip.add(this_user)
    return redirect ('/travels')

def add_plan(request):
    return render(request, 'travel_app/add_plan.html')

def validate_plan(request):
    errors = Trip.objects.plan_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/travels/add/')
    else:
        this_user = User.objects.get(id=request.session['logged_in_user_id'])
        this_trip = Trip.objects.create(destination = request.POST['destination'], travel_start_date=request.POST['travel_start_date'], travel_end_date=request.POST['travel_end_date'], plan=request.POST['plan'], planned_by=this_user)
        this_trip.users_on_trip.add(this_user)
        return redirect('/travels')

def destination(request, number):
    this_trip = Trip.objects.get(id=number)
    context = {
        'this_trip': this_trip,
        'this_trip_users': User.objects.filter(trips_joining=number), 
        'this_trip_planner': User.objects.get(trips_planned=this_trip),
        'this_trip_comments': Comment.objects.filter(trip=this_trip)
    }
    return render(request, 'travel_app/destination.html', context)

def logout(request):
    request.session.clear()
    return redirect('/')





def validate_comment(request, number):
    this_user = User.objects.get(id=request.session['logged_in_user_id'])
    this_trip = Trip.objects.get(id=number)
    users_on_trip = User.objects.filter(trips_joining=number)
    errors = Comment.objects.comment_validator(request.POST, this_trip, this_user, users_on_trip)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect(f'/travels/destination/{number}')    # does this work?
    else:
        this_comment = Comment.objects.create(body=request.POST['body'], user=this_user, trip=this_trip)
        return redirect(f'/travels/destination/{number}')    # does this work?



