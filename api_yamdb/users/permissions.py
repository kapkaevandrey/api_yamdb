from rest_framework import permissions

from .models import User


class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        print(request.user.role)
        return (
            request.user.is_superuser
            or request.user.role == User.ADMIN
        )

    def has_object_permission(self, request, view, obj):
        return (
            request.user.is_superuser
            or request.user.role == User.ADMIN
        )