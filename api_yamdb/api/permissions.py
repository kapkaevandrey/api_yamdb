from rest_framework import permissions


class CategoryGenryTitlePermissions(permissions.BasePermission):
    """Фильтр - разрешает GET запросы всем, остальное только для ADMIN"""
    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or (request.user.is_authenticated
                    and request.user.role == request.user.ADMIN))
