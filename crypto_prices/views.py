from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from .models import Cryptocurrency
import requests
import json
from datetime import datetime, timedelta

# Note: COIN_ID_MAP is no longer needed here as we use crypto.coingecko_id directly
COINGECKO_API_BASE_URL = "https://api.coingecko.com/api/v3"

def fetch_historical_data(coin_id, days=30, vs_currency='usd'):
    """Fetches historical OHLCV data from CoinGecko API."""
    if not coin_id: # Ensure coin_id is not empty
        print("Error: No CoinGecko ID provided for historical data fetch.")
        return None

    url = f"{COINGECKO_API_BASE_URL}/coins/{coin_id}/ohlc"
    params = {
        'vs_currency': vs_currency,
        'days': days,
    }
    # print(f"Fetching historical data for CoinGecko ID: {coin_id} from URL: {url} with params: {params}") # Debug print
    try:
        response = requests.get(url, params=params)
        response.raise_for_status() # Raise HTTPError for bad responses (4xx or 5xx)
        data = response.json()
        # print(f"Successfully fetched {len(data)} data points for {coin_id}") # Debug print
        return data
    except requests.exceptions.RequestException as e:
        print(f"Error fetching historical data for {coin_id}: {e}")
        return None
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON response for {coin_id}: {e}")
        return None

def home_view(request):
    # Fetch top cryptocurrencies, e.g., by market cap, for the trending section
    # Order by market_cap_rank, which is populated by fetch_crypto_prices
    trending_cryptos = Cryptocurrency.objects.exclude(market_cap__isnull=True).order_by('market_cap_rank')[:5]
    context = {
        'trending_cryptos': trending_cryptos,
    }
    return render(request, 'home.html', context)

def crypto_list(request):
    query = request.GET.get('q')

    if query:
        cryptos = Cryptocurrency.objects.filter(
            Q(name__icontains=query) | Q(symbol__icontains=query)
        ).order_by('market_cap_rank') # MODIFIED: Order by market_cap_rank
    else:
        # MODIFIED: Order by market_cap_rank for the default list
        # Exclude those without a rank if you want a clean list
        cryptos = Cryptocurrency.objects.exclude(market_cap_rank__isnull=True).order_by('market_cap_rank')

    context = {'cryptos': cryptos}
    return render(request, 'crypto_prices/crypto_list.html', context)

def crypto_detail(request, pk):
    crypto = get_object_or_404(Cryptocurrency, pk=pk)

    # MODIFIED: Use the stored coingecko_id directly
    coingecko_id_for_api = crypto.coingecko_id

    historical_data = fetch_historical_data(coingecko_id_for_api)
    if historical_data is None:
        historical_data = []

    context = {'crypto': crypto, 'historical_data': historical_data}
    return render(request, 'crypto_prices/crypto_detail.html', context)
