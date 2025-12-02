# ==============================================================================
# 6.5 APP: PRODUCTS (Views ACTUALIZADO)
# Archivo destino: apps/products/views.py
# ==============================================================================
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
        # Requisito: Multi-tenancy (Solo data de mi empresa)
        return Product.objects.filter(company=self.request.user.company)

class InventoryViewSet(viewsets.ModelViewSet):
    serializer_class = InventorySerializer
    permission_classes = [IsAuthenticated, IsGerenteOrHigher]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['branch', 'product']

    def get_queryset(self):
        return Inventory.objects.filter(branch__company=self.request.user.company)

# Requisito PDF: Gestión de Proveedores
class SupplierViewSet(viewsets.ModelViewSet):
    serializer_class = SupplierSerializer
    permission_classes = [IsAuthenticated, IsGerenteOrHigher]

    def get_queryset(self):
        return Supplier.objects.filter(company=self.request.user.company)

# Requisito PDF: Gestión de Sucursales (Solo Admin Cliente)
class BranchViewSet(viewsets.ModelViewSet):
    serializer_class = BranchSerializer
    permission_classes = [IsAuthenticated, IsAdminCliente]

    def get_queryset(self):
        return Branch.objects.filter(company=self.request.user.company)