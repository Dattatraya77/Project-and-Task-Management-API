from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsStaffOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return request.user or request.user.is_staff


class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and request.user.profile.role == "admin"
        )


class IsManagerOrIsAdmin(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and request.user.profile.role in ["admin", "manager"]
        )


class IsUserOrAbove(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated