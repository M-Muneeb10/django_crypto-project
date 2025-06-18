# myfirstproject/crypto_live/views.py

import requests
from django.shortcuts import render
from django.conf import settings # To access API keys from settings if needed later

def crypto_price_list(request):
    api_url = "https://api.coingecko.com/api/v3/coins/markets"
    params = {
        'vs_currency': 'usd', # Currency to compare against (e.g., USD, PKR)
        'order': 'market_cap_desc', # Order by market capitalization (highest first)
        'per_page': 100, # Number of results per page
        'page': 1, # Page number
        'sparkline': False, # No sparkline data needed for now
        # 'price_change_percentage': '1h,24h,7d', # Optional: include price change percentage
    }

    try:
        response = requests.get(api_url, params=params, timeout=10) # 10-second timeout
        response.raise_for_status() # Raise an HTTPError for bad responses (4xx or 5xx)
        crypto_data = response.json()
    except requests.exceptions.RequestException as e:
        # Handle API request errors (e.g., network issues, API down)
        print(f"Error fetching crypto data: {e}")
        crypto_data = [] # Return empty list if API call fails
        # Optionally add a message to the user: messages.error(request, "Could not fetch crypto data at this time.")

    context = {
        'crypto_data': crypto_data,
    }
    return render(request, 'crypto_live/crypto_price_list.html', context)