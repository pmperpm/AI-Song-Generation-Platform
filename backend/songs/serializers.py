from rest_framework import serializers
from users.serializers import UserSerializer
from .models import Song


class SongSerializer(serializers.ModelSerializer):
    owner = UserSerializer(read_only=True)
    is_public = serializers.BooleanField(read_only=True)
    is_complete = serializers.BooleanField(read_only=True)

    class Meta:
        model = Song
        fields = [
            "id", "owner", "title", "genre", "mood", "occasion", "story",
            "lyrics", "language", "status", "visibility", "duration",
            "cover_image", "audio_file", "is_public", "is_complete",
            "created_at", "updated_at",
        ]
        read_only_fields = ["id", "owner", "status", "duration", "audio_file", "created_at", "updated_at"]


class SongCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Song
        fields = ["id", "title", "genre", "mood", "occasion", "story", "lyrics", "language"]
        read_only_fields = ["id"]

    def create(self, validated_data):
        request = self.context.get("request")
        return Song.objects.create(owner=request.user, **validated_data)


class SongUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Song
        fields = ["title", "mood", "occasion", "visibility", "cover_image"]