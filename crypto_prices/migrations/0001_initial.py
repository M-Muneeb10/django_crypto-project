# Generated by Django 5.2.1 on 2025-05-23 05:34

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Cryptocurrency',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('symbol', models.CharField(max_length=10)),
                ('coingecko_id', models.CharField(blank=True, max_length=50, null=True, unique=True)),
                ('current_price', models.DecimalField(blank=True, decimal_places=8, max_digits=20, null=True)),
                ('market_cap', models.DecimalField(blank=True, decimal_places=2, max_digits=30, null=True)),
                ('logo_url', models.URLField(blank=True, max_length=255, null=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('price_change_24h', models.DecimalField(blank=True, decimal_places=8, max_digits=20, null=True)),
                ('price_change_percentage_24h', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('sparkline_data_7d', models.TextField(blank=True, null=True)),
                ('market_cap_rank', models.IntegerField(blank=True, null=True)),
            ],
            options={
                'verbose_name_plural': 'Cryptocurrencies',
            },
        ),
    ]
