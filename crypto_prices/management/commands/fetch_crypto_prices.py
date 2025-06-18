import requests
from django.core.management.base import BaseCommand
from crypto_prices.models import Cryptocurrency
import time
import json # Import json for better debugging

# This map is used to get the CoinGecko ID for certain symbols that don't directly
# match their lowercase symbol (e.g., 'ETH' -> 'ethereum').
# We can expand this list as needed, or update the logic if CoinGecko adds a direct symbol-to-ID mapping.
COIN_ID_MAP = {
    'BTC': 'bitcoin',
    'ETH': 'ethereum',
    'XRP': 'ripple', # XRP's ID is 'ripple' on CoinGecko
    'LTC': 'litecoin',
    'ADA': 'cardano',
    'SOL': 'solana',
    'DOT': 'polkadot',
    'DOGE': 'dogecoin',
    'SHIB': 'shiba-inu',
    'AVAX': 'avalanche',
    'TRX': 'tron', # Adding Tron as it's often in top 100
    # Add more as you discover discrepancies or want to ensure specific coins are included
}

class Command(BaseCommand):
    help = 'Fetches current cryptocurrency prices from CoinGecko API and updates the database.'

    def handle(self, *args, **kwargs):
        self.stdout.write("Fetching cryptocurrency prices from CoinGecko API...")
        coingecko_api_url = "https://api.coingecko.com/api/v3/coins/markets"
        params = {
            'vs_currency': 'usd',
            'order': 'market_cap_desc', # Order by market cap, descending
            'per_page': 100,             # Fetch top 100 cryptocurrencies
            'page': 1,                   # First page of results
            'sparkline': True,           # Include 7-day sparkline data for homepage
            'price_change_percentage': '1h,24h,7d' # Include relevant price changes
        }

        try:
            response = requests.get(coingecko_api_url, params=params)
            response.raise_for_status() # Raise an exception for HTTP errors (4xx or 5xx)
            data = response.json()

            if not data:
                self.stdout.write(self.style.WARNING("No data received from CoinGecko API."))
                return

            for coin_data in data:
                coin_id = coin_data.get('id')
                symbol = coin_data.get('symbol', '').upper()
                name = coin_data.get('name')
                current_price = coin_data.get('current_price')
                market_cap = coin_data.get('market_cap')
                price_change_percentage_24h = coin_data.get('price_change_percentage_24h_in_currency') or coin_data.get('price_change_percentage_24h')
                logo_url = coin_data.get('image')
                sparkline_data = coin_data.get('sparkline_in_7d', {}).get('price', [])
                market_cap_rank = coin_data.get('market_cap_rank')

                # For description, we need a separate call to /coins/{id}
                # To avoid hitting rate limits, we'll fetch description only if it's missing
                # or for the first few coins. For top 100, fetching all descriptions in one go
                # might hit the free tier rate limit of 30 calls/minute.
                # For now, we'll leave description as a placeholder or fetch it for a few only.
                # The existing description field in the model can be populated by a separate, less frequent process.
                description = "" # Placeholder for now

                # Try to get the actual CoinGecko ID for consistency, falling back to symbol.lower()
                # for detail page historical data
                mapped_coingecko_id = COIN_ID_MAP.get(symbol, coin_id)

                cryptocurrency, created = Cryptocurrency.objects.update_or_create(
                    coingecko_id=mapped_coingecko_id, # Use mapped_coingecko_id as primary identifier
                    defaults={
                        'symbol': symbol,
                        'name': name,
                        'current_price': current_price,
                        'market_cap': market_cap,
                        'price_change_percentage_24h': price_change_percentage_24h,
                        'logo_url': logo_url,
                        'sparkline_data_7d': json.dumps(sparkline_data), # Corrected field name and added json.dumps
                        'market_cap_rank': market_cap_rank,
                        'description': description, # Will remain empty unless fetched separately
                    }
                )

                if created:
                    self.stdout.write(self.style.SUCCESS(f"Added {name} ({symbol}) to the database."))
                else:
                    self.stdout.write(self.style.SUCCESS(f"Updated {name} ({symbol}) in the database."))

            self.stdout.write(self.style.SUCCESS("Cryptocurrency data fetching complete."))

        except requests.exceptions.RequestException as e:
            self.stdout.write(self.style.ERROR(f"Error fetching data from CoinGecko API: {e}"))
        except json.JSONDecodeError as e:
            self.stdout.write(self.style.ERROR(f"Error decoding JSON response from CoinGecko API: {e}. Response: {response.text[:200]}...")) # Print first 200 chars of response
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"An unexpected error occurred: {e}"))

        # Add a delay to respect API rate limits if this command is run frequently
        time.sleep(5) # Wait for 5 seconds
