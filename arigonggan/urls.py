from django.urls import path
from . import views
from django.contrib import auth
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.shortcuts import render, redirect

from django.contrib.auth import views as auth_views

app_name = 'arigonggan'
urlpatterns = [
    path('', views.index),
    path('signUp', views.logIn),
    path('delete', views.delete),
    path('reservation', views.reservation),
]