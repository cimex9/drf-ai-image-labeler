from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from app.models import Label, Image

User = get_user_model()


@admin.register(User)
class UserAdmin(BaseUserAdmin): ...

@admin.register(Label)
class LabelAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)

@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ("id", "file", "created_at", "processed_at")
    list_filter = ("created_at",)
    search_fields = ("file",)
