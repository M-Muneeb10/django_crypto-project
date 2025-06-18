# myfirstproject/quick_updates/forms.py

from django import forms
from .models import Subscriber

class SubscriberForm(forms.ModelForm):
    email = forms.EmailField(
        label='Your Email',
        max_length=254,
        widget=forms.EmailInput(attrs={
            'placeholder': 'Enter your email address',
            'class': 'w-full px-3 py-2 bg-gray-700 text-gray-100 rounded-md focus:outline-none focus:ring-blue-500 focus:border-blue-500'
        })
    )

    class Meta:
        model = Subscriber
        fields = ['email']