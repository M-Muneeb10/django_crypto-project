# myfirstproject/quick_updates/admin.py

from django.contrib import admin
from .models import Subscriber

@admin.register(Subscriber)
class SubscriberAdmin(admin.ModelAdmin):
    list_display = ('email', 'date_subscribed')
    search_fields = ('email',)
    list_filter = ('date_subscribed',)
    date_hierarchy = 'date_subscribed'