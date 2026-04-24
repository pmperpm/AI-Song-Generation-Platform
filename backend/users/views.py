from rest_framework import generics, permissions

from .models import User
from .permissions import IsAdminRole, IsOwnerOrAdmin
from .serializers import UserCreateSerializer, UserSerializer, UserUpdateSerializer

from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from dj_rest_auth.registration.views import SocialLoginView
from django.conf import settings


class GoogleLogin(SocialLoginView):
    """
    Handles Google OAuth login. The frontend should send a POST request
    with `access_token` or `code` (if using PKCE).
    """
    adapter_class = GoogleOAuth2Adapter
    callback_url = getattr(settings, "GOOGLE_CALLBACK_URL", "http://localhost:3000")
    client_class = OAuth2Client


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