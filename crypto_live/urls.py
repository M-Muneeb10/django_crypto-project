# myfirstproject/crypto_live/urls.py

from django.urls import path
from . import views

app_name = 'crypto_live' # Set the app namespace to 'crypto_live'

urlpatterns = [
    path('prices/', views.crypto_price_list, name='crypto_price_list'),
]