from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from users.models import Role
from users.permissions import IsAdminRole, IsOwnerOrAdmin
from .models import Song, Status, Visibility
from .serializers import SongCreateSerializer, SongSerializer, SongUpdateSerializer


class SongListCreateView(generics.ListCreateAPIView):
    def get_queryset(self):
        user = self.request.user
        if user and user.is_authenticated:
            if user.role == Role.ADMIN:
                return Song.objects.all()
            return Song.objects.filter(owner=user) | Song.objects.filter(
                visibility=Visibility.PUBLIC, status=Status.COMPLETE
            ).exclude(owner=user)
        return Song.objects.filter(visibility=Visibility.PUBLIC, status=Status.COMPLETE)

    def get_permissions(self):
        if self.request.method == "POST":
            return [permissions.IsAuthenticated()]
        return [permissions.AllowAny()]

    def get_serializer_class(self):
        if self.request.method == "POST":
            return SongCreateSerializer
        return SongSerializer


class SongRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Song.objects.all()
    http_method_names = ["get", "patch", "delete", "head", "options"]

    def get_permissions(self):
        if self.request.method == "GET":
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated(), IsOwnerOrAdmin()]

    def get_serializer_class(self):
        if self.request.method == "PATCH":
            return SongUpdateSerializer
        return SongSerializer

    def get_object(self):
        song = get_object_or_404(Song, pk=self.kwargs["pk"])
        if not self.request.user or not self.request.user.is_authenticated:
            if song.visibility != Visibility.PUBLIC or song.status != Status.COMPLETE:
                self.permission_denied(self.request, message="This song is private or not yet complete.")
        self.check_object_permissions(self.request, song)
        return song


class SongStatusUpdateView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def patch(self, request: Request, pk: int) -> Response:
        song = get_object_or_404(Song, pk=pk)
        IsOwnerOrAdmin().has_object_permission(request, self, song)

        new_status = request.data.get("status")
        duration = request.data.get("duration")

        if new_status not in [s.value for s in Status]:
            return Response(
                {"detail": f"Invalid status. Choose from {[s.value for s in Status]}."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        song.status = new_status
        if duration is not None:
            song.duration = duration
        song.save(update_fields=["status", "duration", "updated_at"])

        return Response(SongSerializer(song).data, status=status.HTTP_200_OK)


@api_view(["GET"])
@permission_classes([permissions.AllowAny])
def public_song_preview(request: Request, pk: int) -> Response:
    song = get_object_or_404(Song, pk=pk, visibility=Visibility.PUBLIC, status=Status.COMPLETE)
    return Response(SongSerializer(song, context={"request": request}).data)


@api_view(["GET"])
@permission_classes([IsAdminRole])
def admin_song_analytics(request: Request) -> Response:
    from django.db.models import Count
    from django.db.models.functions import TruncWeek

    weekly_data = (
        Song.objects.annotate(week=TruncWeek("created_at"))
        .values("week")
        .annotate(count=Count("id"))
        .order_by("week")
    )
    return Response(
        [{"week": entry["week"].strftime("%Y-%m-%d"), "count": entry["count"]} for entry in weekly_data]
    )