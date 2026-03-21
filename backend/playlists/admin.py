from django import forms
from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError

from .models import Playlist
from songs.models import Song, Status

class PlaylistAdminForm(forms.ModelForm):
    class Meta:
        model = Playlist
        fields = "__all__"

    def clean(self):
        cleaned_data = super().clean()
        owner = cleaned_data.get("owner")
        songs = cleaned_data.get("songs")

        if owner and songs:
            invalid_owners = []
            incomplete_songs = []
            
            for song in songs:
                if song.owner_id != owner.id:
                    invalid_owners.append(song.title or f"Song #{song.id}")
                if song.status != Status.COMPLETE:
                    incomplete_songs.append(song.title or f"Song #{song.id}")
            
            errors = {}
            if invalid_owners:
                errors["songs"] = ValidationError(
                    _("You can only add songs owned by the playlist owner. Invalid: %(songs)s"),
                    params={"songs": ", ".join(invalid_owners)}
                )
            if incomplete_songs:
                err_msg = ValidationError(
                    _("Only complete songs can be added. Incomplete: %(songs)s"),
                    params={"songs": ", ".join(incomplete_songs)}
                )
                if "songs" in errors:
                    pass
                else:
                    errors["songs"] = err_msg

            if errors:
                raise ValidationError(errors)
                
        return cleaned_data


@admin.register(Playlist)
class PlaylistAdmin(admin.ModelAdmin):
    form = PlaylistAdminForm
    list_display = ("name", "owner", "song_count", "created_at", "updated_at")
    list_filter = ("created_at",)
    search_fields = ("name", "owner__email")
    ordering = ("-created_at",)
    readonly_fields = ("created_at", "updated_at")
    filter_horizontal = ("songs",)

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        """Restrict songs to only complete ones, and to owner's songs if editing."""
        if db_field.name == "songs":
            qs = Song.objects.filter(status=Status.COMPLETE)
            
            playlist_id = request.resolver_match.kwargs.get('object_id')
            if playlist_id:
                # show only COMPLETE songs owned by this playlist's owner
                playlist = self.get_object(request, playlist_id)
                if playlist:
                    qs = qs.filter(owner=playlist.owner)
            else:
                # only show complete songs owned by the current user when creating a new playlist
                pass
                
            kwargs["queryset"] = qs
            
        return super().formfield_for_manytomany(db_field, request, **kwargs)

    @admin.display(description=_("# Songs"))
    def song_count(self, obj):
        return obj.songs.count()