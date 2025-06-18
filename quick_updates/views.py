# myfirstproject/quick_updates/views.py

from django.shortcuts import render, redirect
from django.contrib import messages # For displaying success/error messages
from .forms import SubscriberForm

def subscribe_newsletter(request):
    if request.method == 'POST':
        form = SubscriberForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, 'Thank you for subscribing to quick updates!')
                return redirect('blog:post_list') # Redirect to blog homepage after successful subscription
            except Exception as e:
                # Handle cases where email already exists (due to unique=True)
                # Check for specific database integrity error for unique constraint violation
                if 'unique constraint' in str(e).lower() or 'duplicate key' in str(e).lower():
                    messages.warning(request, 'This email address is already subscribed.')
                else:
                    messages.error(request, 'There was an error with your subscription. Please try again.')
                return redirect('blog:post_list')
        else:
            messages.error(request, 'Please enter a valid email address.')
            # If form is not valid, redirect back and let messages display the error
            return redirect('blog:post_list')
    else:
        # This view is primarily for POST requests from the embedded form.
        # If accessed directly via GET, it would typically show a dedicated subscribe page,
        # but for this setup, we just provide an empty form.
        form = SubscriberForm()
        return render(request, 'quick_updates/subscribe.html', {'form': form})