from django import forms
from django.contrib.auth import get_user_model

from accounts.models import UserProfile

User = get_user_model()


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "email"]


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ["profile_picture", "bio", "website", "linkedin", "github"]
        widgets = {"bio": forms.Textarea(attrs={"rows": 4})}
