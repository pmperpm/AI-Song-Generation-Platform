from rest_framework import serializers
from users.serializers import UserSerializer
from songs.serializers import SongSerializer
from songs.models import Song
from .models import Playlist
 
class PlaylistSerializer(serializers.ModelSerializer):
    owner = UserSerializer(read_only=True)
    songs = SongSerializer(many=True, read_only=True)
    song_count = serializers.IntegerField(source="songs.count", read_only=True)

    class Meta:
        model = Playlist
        fields = ["id", "owner", "name", "songs", "song_count", "created_at", "updated_at"]
        read_only_fields = ["id", "owner", "created_at", "updated_at"]


class PlaylistCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Playlist
        fields = ["id", "name"]
        read_only_fields = ["id"]

    def create(self, validated_data):
        request = self.context.get("request")
        return Playlist.objects.create(owner=request.user, **validated_data)


class PlaylistUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Playlist
        fields = ["name"]


class PlaylistSongSerializer(serializers.Serializer):
    song_id = serializers.PrimaryKeyRelatedField(queryset=Song.objects.all())