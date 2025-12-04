from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from .models import Product, Inventory, Supplier, Branch
from .serializers import ProductSerializer, InventorySerializer, SupplierSerializer, BranchSerializer
from apps.users.permissions import IsGerenteOrHigher, IsVendedorOrHigher, IsAdminCliente

class ProductViewSet(viewsets.ModelViewSet):
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated, IsVendedorOrHigher] 
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['category', 'sku']

    def get_queryset(self):
        user = self.request.user
        # LÓGICA DE ROLES CORREGIDA:
        # 1. Super Admin: Acceso total a la base de datos
        if user.role == 'SUPER_ADMIN':
            return Product.objects.all()
        # 2. Usuarios de Empresa: Acceso acotado a su tenant
        if user.company:
            return Product.objects.filter(company=user.company)
        # 3. Usuario huérfano (seguridad): Lista vacía
        return Product.objects.none()

class InventoryViewSet(viewsets.ModelViewSet):
    serializer_class = InventorySerializer
    permission_classes = [IsAuthenticated, IsGerenteOrHigher]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['branch', 'product']

    def get_queryset(self):
        user = self.request.user
        if user.role == 'SUPER_ADMIN':
            return Inventory.objects.all()
        if user.company:
            return Inventory.objects.filter(branch__company=user.company)
        return Inventory.objects.none()
    
class SupplierViewSet(viewsets.ModelViewSet):
    serializer_class = SupplierSerializer
    permission_classes = [IsAuthenticated, IsGerenteOrHigher]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'SUPER_ADMIN':
            return Supplier.objects.all()
        if user.company:
            return Supplier.objects.filter(company=user.company)
        return Supplier.objects.none()

class BranchViewSet(viewsets.ModelViewSet):
    serializer_class = BranchSerializer
    permission_classes = [IsAuthenticated, IsAdminCliente]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'SUPER_ADMIN':
            return Branch.objects.all()
        if user.company:
            return Branch.objects.filter(company=user.company)
        return Branch.objects.none()