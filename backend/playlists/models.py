from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError


class Playlist(models.Model):
    owner = models.ForeignKey("users.User", on_delete=models.CASCADE, related_name="playlists")
    name = models.CharField(max_length=255)
    songs = models.ManyToManyField("songs.Song", related_name="playlists", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Playlist")
        verbose_name_plural = _("Playlists")
        ordering = ["-created_at"]
        unique_together = [("owner", "name")]

    def __str__(self):
        return f"{self.name} (by {self.owner.email})"