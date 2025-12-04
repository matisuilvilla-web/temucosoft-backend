from rest_framework import permissions

class IsSuperAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'SUPER_ADMIN'

class IsAdminCliente(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'ADMIN_CLIENTE'

class IsGerenteOrHigher(permissions.BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated: return False
        return request.user.role in ['GERENTE', 'ADMIN_CLIENTE', 'SUPER_ADMIN']

class IsVendedorOrHigher(permissions.BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated: return False
        return request.user.role in ['VENDEDOR', 'GERENTE', 'ADMIN_CLIENTE', 'SUPER_ADMIN']