from django.urls import path
from . import views

app_name = "songs"

urlpatterns = [
    path("songs/", views.SongListCreateView.as_view(), name="song-list-create"),
    path("songs/<int:pk>/", views.SongRetrieveUpdateDestroyView.as_view(), name="song-detail"),
    path("songs/<int:pk>/status/", views.SongStatusUpdateView.as_view(), name="song-status-update"),
    path("songs/public/<int:pk>/", views.public_song_preview, name="song-public-preview"),
    path("admin/analytics/songs/", views.admin_song_analytics, name="admin-analytics-songs"),
]