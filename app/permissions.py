from rest_framework import permissions

class IsClientOrAdmin(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.client == request.user or request.user.is_admin

# Обновляем во ViewSet:
permission_classes = [IsClientOrAdmin]