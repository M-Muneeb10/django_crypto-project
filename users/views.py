# myfirstproject/users/views.py
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import CustomUserCreationForm # Import our custom form

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account created successfully! You can now log in.')
            return redirect('login') # Redirect to the login page
    else:
        form = CustomUserCreationForm()
    return render(request, 'users/register.html', {'form': form})