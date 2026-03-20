from rest_framework import permissions
from .models import Role


class IsAdminRole(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.role == Role.ADMIN


class IsOwnerOrAdmin(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.role == Role.ADMIN:
            return True
        return obj.owner == request.user