from rest_framework import permissions


class IsAdminUserOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow admin users to create, update, or delete books.
    All users (even unauthenticated) can view the books.
    """

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            # Allow all users to read (GET) books
            return True
        # Check if the user is an admin for other methods (POST, PUT, DELETE)
        return request.user and request.user.is_staff
