from rest_framework import serializers
from users.serializers import UserSerializer
from .models import Song


class SongSerializer(serializers.ModelSerializer):
    owner = UserSerializer(read_only=True)
    is_public = serializers.BooleanField(read_only=True)
    is_complete = serializers.BooleanField(read_only=True)
    audio_url = serializers.SerializerMethodField()
    cover_url = serializers.SerializerMethodField()

    class Meta:
        model = Song
        fields = [
            "id", "owner", "title", "genre", "mood", "occasion", "story",
            "lyrics", "language", "status", "visibility", "duration",
            "cover_image", "audio_file", "audio_url", "cover_url", 
            "is_public", "is_complete", "created_at", "updated_at",
        ]
        read_only_fields = ["id", "owner", "status", "duration", "audio_file", "created_at", "updated_at"]

    def get_audio_url(self, obj):
        request = self.context.get("request")
        if obj.audio_file and request:
            return request.build_absolute_uri(obj.audio_file.url)
        return None

    def get_cover_url(self, obj):
        request = self.context.get("request")
        if obj.cover_image and request:
            return request.build_absolute_uri(obj.cover_image.url)
        return None


class SongCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Song
        fields = ["id", "title", "genre", "mood", "occasion", "story", "lyrics", "language"]
        read_only_fields = ["id"]

    def create(self, validated_data):
        # Allow owner and status to be passed in from the view's serializer.save() call
        return Song.objects.create(**validated_data)


class SongUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Song
        fields = ["title", "mood", "occasion", "visibility", "cover_image"]