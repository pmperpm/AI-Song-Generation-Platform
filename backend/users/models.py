from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class Role(models.TextChoices):
    USER  = "user",  _("User")
    ADMIN = "admin", _("Admin")


class User(AbstractUser):
    id = models.AutoField(primary_key=True)
    email = models.EmailField(_("email address"), unique=True)
    role = models.CharField(max_length=10, choices=Role.choices, default=Role.USER)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    class Meta:
        verbose_name = _("User")
        verbose_name_plural = _("Users")
        ordering = ["-date_joined"]

    @property
    def name(self):
        return self.username

    @property
    def is_admin_role(self):
        return self.role == Role.ADMIN

    def __str__(self):
        return f"{self.email} ({self.get_role_display()})"