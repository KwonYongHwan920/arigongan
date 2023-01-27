from django.urls import path
from . import views
from django.contrib import auth
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.shortcuts import render, redirect

from django.contrib.auth import views as auth_views

app_name = 'arigonggan'
urlpatterns=[
    path('logIn',views.signIn),
    path('reservation',views.postReservation),
    path('all',views.seatStatusList),
    path('delete', views.delete),
    path('auto-delete', views.autoDelete),
    path('user-reservation', views.userReservation),
    path('booked', views.booked),
    path('reservationList', views.reserveList),
    path('disable', views.allSeatDisable),
    path('activate',views.allSeatActivate),
]