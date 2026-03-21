from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ["id", "email", "username", "role", "date_joined"]
        read_only_fields = ["id", "date_joined"]

    def get_name(self, obj):
        return obj.name


class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "email", "username", "role"]
        read_only_fields = ["id"]

    def create(self, validated_data):
        return User.objects.create(**validated_data)


class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "role"]