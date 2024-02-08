from rest_framework import permissions


class IsAdminUserOrReadAndCreateOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        if request.method in ["GET", "HEAD", "OPTIONS", "POST"]:
            return True
        if request.user.is_staff:
            return True
        return False
