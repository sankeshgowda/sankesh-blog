from django import forms

from newsletter.models import NewsletterSubscriber


class NewsletterSubscriberForm(forms.ModelForm):
    class Meta:
        model = NewsletterSubscriber
        fields = ["email"]
        widgets = {"email": forms.EmailInput(attrs={"placeholder": "you@example.com"})}
