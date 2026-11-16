from rest_framework import permissions
class IsAdminOrCreateReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        # Allow safe methods (GET, HEAD, OPTIONS) for any request
        if request.method in permissions.SAFE_METHODS:
            return True
        # Check if the user is an admin for write operations (POST)
        return request.user and request.user.is_staff