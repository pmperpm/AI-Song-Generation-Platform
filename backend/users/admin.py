from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _

from .models import User


class CustomUserCreationForm(forms.ModelForm):
    """Custom form for creating users without password (OAuth only)."""
    role = forms.ChoiceField(choices=User._meta.get_field('role').choices)
    
    class Meta:
        model = User
        fields = ("username", "email", "role")

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("A user with this email already exists.")
        return email


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ("email", "username", "role", "is_staff", "is_active", "date_joined")
    list_filter = ("role", "is_staff", "is_active", "date_joined")
    search_fields = ("email", "username")
    ordering = ("-date_joined",)
    
    add_form = CustomUserCreationForm

    fieldsets = (
        (None, {"fields": ("username", "email")}),
        (_("Platform Role"), {"fields": ("role",)}),
        (_("Permissions"), {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")}),
        (_("Important Dates"), {"fields": ("last_login", "date_joined")}),
    )

    add_fieldsets = (
        (None, {"classes": ("wide",), "fields": ("username", "email", "role")}),
    )

    def save_model(self, request, obj, form, change):
        """Override save to set a random unusable password for OAuth-only users."""
        if not change:  # Adding new user
            obj.set_unusable_password()
        super().save_model(request, obj, form, change)