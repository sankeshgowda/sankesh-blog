from django.contrib import admin

from accounts.models import UserProfile


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "website", "created_at")
    search_fields = ("user__username", "user__email", "bio")
