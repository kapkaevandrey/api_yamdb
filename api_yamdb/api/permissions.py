from rest_framework import permissions


class CategoryGenryTitlePermissions(permissions.BasePermission):
    """Фильтр - разрешает GET запросы всем, остальное только для ADMIN"""

    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or (request.user.is_authenticated
                    and request.user.role == request.user.ADMIN))


class AuthorAdminModeratorOrReadOnly(permissions.BasePermission):
    """Разрешение на чтение для всех пользователей.
    Редактирование, обновление или удаление разрешено только
    авторам, модераторам и администраторам."""

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        object_author = obj.author == request.user
        admin_or_moderator = (
                request.user.is_authenticated
                and (request.user.role == request.user.ADMIN
                     or request.user.role == request.user.MODERATOR))
        return object_author or admin_or_moderator or request.user.is_staff or request.user.is_superuser
    # TODO вынести определение свойства в отдельный метод
