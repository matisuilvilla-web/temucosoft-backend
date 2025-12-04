from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from .models import Product, Inventory, Supplier, Branch
from .serializers import ProductSerializer, InventorySerializer, SupplierSerializer, BranchSerializer
from apps.users.permissions import IsGerenteOrHigher, IsVendedorOrHigher, IsAdminCliente
from utils.mixins import MultiTenantModelMixin  # Importamos el archivo de arriba

class ProductViewSet(MultiTenantModelMixin, viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated, IsVendedorOrHigher] 
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['category', 'sku']

class InventoryViewSet(MultiTenantModelMixin, viewsets.ModelViewSet):
    queryset = Inventory.objects.all()
    serializer_class = InventorySerializer
    permission_classes = [IsAuthenticated, IsGerenteOrHigher]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['branch', 'product']

class SupplierViewSet(MultiTenantModelMixin, viewsets.ModelViewSet):
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer
    permission_classes = [IsAuthenticated, IsGerenteOrHigher]

class BranchViewSet(MultiTenantModelMixin, viewsets.ModelViewSet):
    queryset = Branch.objects.all()
    serializer_class = BranchSerializer
    permission_classes = [IsAuthenticated, IsVendedorOrHigher]