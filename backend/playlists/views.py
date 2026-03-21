from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions, status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from users.models import Role
from users.permissions import IsOwnerOrAdmin
from .models import Playlist
from .serializers import PlaylistCreateSerializer, PlaylistSerializer, PlaylistSongSerializer, PlaylistUpdateSerializer


class PlaylistListCreateView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if self.request.user.role == Role.ADMIN:
            return Playlist.objects.all()
        return Playlist.objects.filter(owner=self.request.user)

    def get_serializer_class(self):
        if self.request.method == "POST":
            return PlaylistCreateSerializer
        return PlaylistSerializer


class PlaylistRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Playlist.objects.all()
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrAdmin]
    http_method_names = ["get", "patch", "delete", "head", "options"]

    def get_serializer_class(self):
        if self.request.method == "PATCH":
            return PlaylistUpdateSerializer
        return PlaylistSerializer


class PlaylistSongAddView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrAdmin]

    def post(self, request: Request, pk: int) -> Response:
        playlist = get_object_or_404(Playlist, pk=pk)
        self.check_object_permissions(request, playlist)
        serializer = PlaylistSongSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        playlist.songs.add(serializer.validated_data["song_id"])
        return Response(PlaylistSerializer(playlist, context={"request": request}).data, status=status.HTTP_200_OK)


class PlaylistSongRemoveView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrAdmin]

    def post(self, request: Request, pk: int) -> Response:
        playlist = get_object_or_404(Playlist, pk=pk)
        self.check_object_permissions(request, playlist)
        serializer = PlaylistSongSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        playlist.songs.remove(serializer.validated_data["song_id"])
        return Response(PlaylistSerializer(playlist, context={"request": request}).data, status=status.HTTP_200_OK)