# myfirstproject/users/urls.py
from django.urls import path
from . import views

app_name = 'users' # App namespace for the users app

urlpatterns = [
    path('register/', views.register, name='register'),
]