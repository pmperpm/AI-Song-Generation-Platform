from django.db import models
from django.utils.translation import gettext_lazy as _


class Genre(models.TextChoices):
    JAZZ       = "jazz",       _("Jazz")
    POP        = "pop",        _("Pop")
    ELECTRONIC = "electronic", _("Electronic")
    ROCK       = "rock",       _("Rock")


class Status(models.TextChoices):
    GENERATING = "generating", _("Generating")
    COMPLETE   = "complete",   _("Complete")
    FAIL       = "fail",       _("Fail")


class Visibility(models.TextChoices):
    PUBLIC  = "public",  _("Public")
    PRIVATE = "private", _("Private")
    

class Song(models.Model):
    owner = models.ForeignKey("users.User", on_delete=models.CASCADE, related_name="songs")
    title = models.CharField(max_length=255, blank=True, default="")
    genre = models.CharField(max_length=20, choices=Genre.choices)
    mood = models.CharField(max_length=100, blank=True, default="")
    occasion = models.CharField(max_length=100, blank=True, default="")
    story = models.TextField(max_length=2000)
    lyrics = models.CharField(max_length=5000, blank=True, default="")
    language = models.CharField(max_length=50, blank=True, default="English")
    status = models.CharField(max_length=15, choices=Status.choices, default=Status.GENERATING)
    visibility = models.CharField(max_length=10, choices=Visibility.choices, default=Visibility.PRIVATE)
    duration = models.PositiveIntegerField(null=True, blank=True)
    cover_image = models.ImageField(upload_to="covers/", null=True, blank=True)
    audio_file = models.FileField(upload_to="audio/", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Song")
        verbose_name_plural = _("Songs")
        ordering = ["-created_at"]

    def __str__(self):
        title_display = self.title or f"Song #{self.pk}"
        return f"{title_display} — {self.owner.email} [{self.get_status_display()}]"

    @property
    def is_public(self):
        return self.visibility == Visibility.PUBLIC

    @property
    def is_complete(self):
        return self.status == Status.COMPLETE