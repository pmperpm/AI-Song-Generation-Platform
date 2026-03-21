from django.urls import path
from . import views

app_name = "playlists"

urlpatterns = [
    path("playlists/", views.PlaylistListCreateView.as_view(), name="playlist-list-create"),
    path("playlists/<int:pk>/", views.PlaylistRetrieveUpdateDestroyView.as_view(), name="playlist-detail"),
    path("playlists/<int:pk>/songs/add/", views.PlaylistSongAddView.as_view(), name="playlist-song-add"),
    path("playlists/<int:pk>/songs/remove/", views.PlaylistSongRemoveView.as_view(), name="playlist-song-remove"),
]