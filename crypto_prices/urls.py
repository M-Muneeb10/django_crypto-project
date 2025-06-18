from django.urls import path
from . import views # Import views from the current app

urlpatterns = [
    # This maps the root of the crypto_prices app to the home_view.
    # Because myfirstproject/urls.py includes this at '',
    # this makes home_view accessible at the project's root '/'.
    path('', views.home_view, name='home'),

    # This maps /cryptos/ to the crypto_list view.
    # Because myfirstproject/urls.py includes this at '',
    # this makes crypto_list accessible at /cryptos/
    path('cryptos/', views.crypto_list, name='crypto_list'),

    # This maps /cryptos/<pk>/ to the crypto_detail view.
    # Because myfirstproject/urls.py includes this at '',
    # this makes crypto_detail accessible at /cryptos/<pk>/
    path('cryptos/<int:pk>/', views.crypto_detail, name='crypto_detail'),
]
