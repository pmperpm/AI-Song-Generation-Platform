from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _

from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ("email", "username", "get_full_name", "role", "is_staff", "is_active", "date_joined")
    list_filter = ("role", "is_staff", "is_active", "date_joined")
    search_fields = ("email", "username", "first_name", "last_name")
    ordering = ("-date_joined",)

    fieldsets = (
        (None, {"fields": ("username", "email", "password")}),
        (_("Personal Info"), {"fields": ("first_name", "last_name")}),
        (_("Platform Role"), {"fields": ("role",)}),
        (_("Permissions"), {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")}),
        (_("Important Dates"), {"fields": ("last_login", "date_joined")}),
    )

    add_fieldsets = (
        (None, {"classes": ("wide",), "fields": ("username", "email", "password1", "password2", "role")}),
    )