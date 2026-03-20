from rest_framework import generics, permissions

from .models import User
from .permissions import IsAdminRole, IsOwnerOrAdmin
from .serializers import UserCreateSerializer, UserSerializer, UserUpdateSerializer


class UserListCreateView(generics.ListCreateAPIView):
    queryset = User.objects.all().order_by("-date_joined")

    def get_permissions(self):
        if self.request.method == "POST":
            return [permissions.AllowAny()]
        return [IsAdminRole()]

    def get_serializer_class(self):
        if self.request.method == "POST":
            return UserCreateSerializer
        return UserSerializer


class UserRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()

    def get_permissions(self):
        return [permissions.IsAuthenticated(), IsOwnerOrAdmin()]

    def get_serializer_class(self):
        if self.request.method in ("PUT", "PATCH"):
            return UserUpdateSerializer
        return UserSerializer