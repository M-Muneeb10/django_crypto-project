# myfirstproject/quick_updates/context_processors.py

from .forms import SubscriberForm

def subscriber_form(request):
    # This context processor provides an unbound SubscriberForm to all templates.
    # It ensures the form is always available in the context of every rendered template.
    return {'subscriber_form': SubscriberForm()}