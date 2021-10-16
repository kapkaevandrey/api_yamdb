from rest_framework import permissions

from .models import User


class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_superuser
            or request.user.role == User.ADMIN
        )
