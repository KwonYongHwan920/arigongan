from django.urls import path
from . import views

app_name = 'supervisor'
urlpatterns = [
    path('test',views.ntest)
]