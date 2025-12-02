# ==============================================================================
# 11. APP: SALES (Views)
# Archivo destino: apps/sales/views.py
# ==============================================================================
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from .models import Sale
from .serializers import SaleSerializer
from apps.users.permissions import IsVendedorOrHigher

class SaleViewSet(viewsets.ModelViewSet):
    serializer_class = SaleSerializer
    permission_classes = [IsAuthenticated, IsVendedorOrHigher]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['branch', 'payment_method', 'created_at']

    def get_queryset(self):
        # Requisito: Ver solo ventas de mi empresa
        return Sale.objects.filter(branch__company=self.request.user.company)

    def perform_create(self, serializer):
        # Asignar automáticamente el usuario vendedor que hace la petición
        serializer.save(user=self.request.user)