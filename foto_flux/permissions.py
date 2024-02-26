from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Checks whether user has read access by default
    and if not checks if user is the owner of the object
    """
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.owner == request.user