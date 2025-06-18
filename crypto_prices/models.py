from django.db import models

class Cryptocurrency(models.Model):
    name = models.CharField(max_length=100, unique=True)
    # MODIFIED LINE: Removed unique=True from symbol
    symbol = models.CharField(max_length=10)
    coingecko_id = models.CharField(max_length=50, unique=True, null=True, blank=True)
    current_price = models.DecimalField(max_digits=20, decimal_places=8, null=True, blank=True)
    market_cap = models.DecimalField(max_digits=30, decimal_places=2, null=True, blank=True)
    logo_url = models.URLField(max_length=255, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    price_change_24h = models.DecimalField(max_digits=20, decimal_places=8, null=True, blank=True)
    price_change_percentage_24h = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    sparkline_data_7d = models.TextField(null=True, blank=True) # Stores JSON string of prices
    market_cap_rank = models.IntegerField(null=True, blank=True)


    def __str__(self):
        return f"{self.name} ({self.symbol})"

    class Meta:
        verbose_name_plural = "Cryptocurrencies"
