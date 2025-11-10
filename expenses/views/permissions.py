from rest_framework import permissions


class IsOwnerOrAdmin(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        print(obj.creator == request.user)
        return obj.creator == request.user or request.user.is_staff
