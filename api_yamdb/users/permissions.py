from rest_framework import permissions

from .models import Role


class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return (request.user.is_superuser
                    or request.user.is_staff
                    or request.user.role == Role.ADMIN
                    )
        return False
