from rest_framework.permissions import BasePermission

class  CustomPermissionsForProducts(BasePermission):
    def has_permission(self, request, obj):
        return request.user and request.user.is_authenticated
    