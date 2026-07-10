from django.contrib import admin
from .models import Profile

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "follower_count")

    def follower_count(self, obj):
        return obj.followers.count()
