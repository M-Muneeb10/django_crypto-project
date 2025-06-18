# myfirstproject/quick_updates/urls.py

from django.urls import path
from . import views

app_name = 'quick_updates' # Set the app namespace

urlpatterns = [
    path('subscribe/', views.subscribe_newsletter, name='subscribe_newsletter'),
]