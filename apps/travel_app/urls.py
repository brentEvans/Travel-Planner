from django.urls import path
from . import views


urlpatterns = [
    path('', views.index),
    path('register/', views.validate_registration),
    path('login/', views.validate_login),
    path('travels/', views.travels),
    path('travels/add/', views.add_plan),
    path('travels/join/<number>', views.join_trip),
    path('travels/add/validate/', views.validate_plan),
    path('travels/destination/<number>', views.destination),
    path('travels/destination/<number>/validate_comment', views.validate_comment),
    path('logout/', views.logout),
]