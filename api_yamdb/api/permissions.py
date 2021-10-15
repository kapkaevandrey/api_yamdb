from rest_framework import permissions

# class CategoryGenryTitlePermissions(permissions.BasePermission):
#     def has_permission(self, request, view):
#         return (request.method in permissions.SAFE_METHODS or
#                 request.user.role.admin)


class AuthorAdminModeratorOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        object_author = obj.author == request.user
        admin_or_moderator = getattr(request.user, "role", "user") in ['admin', 'moderator']
        return object_author or admin_or_moderator
