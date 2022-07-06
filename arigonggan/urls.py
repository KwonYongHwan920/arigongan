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
    path('signUp', views.signup),
    path('login', views.login),
    path('delete', views.delete),
    # path('login/', auth_views.LoginView.as_view(template_name='arigonggan/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('', views.index, name='index'),  # '/' 에 해당되는 path
]