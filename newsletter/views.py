from django.contrib import messages
from django.shortcuts import redirect
from django.views.decorators.http import require_POST

from newsletter.forms import NewsletterSubscriberForm


@require_POST
def subscribe(request):
    form = NewsletterSubscriberForm(request.POST)
    if form.is_valid():
        form.save()
        messages.success(request, "You are subscribed to Sankesh Blog.")
    else:
        messages.error(request, "Please enter a valid email address.")
    return redirect(request.META.get("HTTP_REFERER", "blog:home"))
