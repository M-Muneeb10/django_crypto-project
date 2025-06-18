from django import forms
from .models import Comment

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('name', 'email', 'body')
        widgets = {
            'name': forms.TextInput(attrs={'class': 'w-full px-3 py-2 placeholder-gray-500 text-gray-900 rounded-md focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm'}),
            'email': forms.EmailInput(attrs={'class': 'w-full px-3 py-2 placeholder-gray-500 text-gray-900 rounded-md focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm'}),
            'body': forms.Textarea(attrs={'class': 'w-full px-3 py-2 placeholder-gray-500 text-gray-900 rounded-md focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm', 'rows': 4}),
        }
        labels = {
            'name': 'Your Name',
            'email': 'Your Email',
            'body': 'Your Comment',
        }