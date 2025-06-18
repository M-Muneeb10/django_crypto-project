# myfirstproject/quick_updates/models.py

from django.db import models

class Subscriber(models.Model):
    email = models.EmailField(unique=True)
    date_subscribed = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email

    class Meta:
        ordering = ['-date_subscribed']
        verbose_name = 'Subscriber'
        verbose_name_plural = 'Subscribers'