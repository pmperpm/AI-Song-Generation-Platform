from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from .models import Song, Status, Visibility


@admin.register(Song)
class SongAdmin(admin.ModelAdmin):
    list_display = ("title_display", "owner", "genre", "mood", "language", "status", "visibility", "duration_display", "created_at")
    list_filter = ("status", "visibility", "genre", "language", "created_at")
    search_fields = ("title", "owner__email", "mood", "occasion", "story", "lyrics")
    ordering = ("-created_at",)
    readonly_fields = ("created_at", "updated_at")
    date_hierarchy = "created_at"
    actions = ["make_private", "mark_failed"]

    @admin.display(description=_("Title"))
    def title_display(self, obj):
        return obj.title or f"(Untitled — #{obj.pk})"

    @admin.display(description=_("Duration"))
    def duration_display(self, obj):
        if obj.duration is None:
            return "—"
        minutes, seconds = divmod(obj.duration, 60)
        return f"{minutes}m {seconds:02d}s"

    @admin.action(description=_("Set selected songs to Private"))
    def make_private(self, request, queryset):
        updated = queryset.update(visibility=Visibility.PRIVATE)
        self.message_user(request, f"{updated} song(s) set to Private.")

    @admin.action(description=_("Mark selected songs as Failed"))
    def mark_failed(self, request, queryset):
        updated = queryset.update(status=Status.FAIL)
        self.message_user(request, f"{updated} song(s) marked as Failed.")