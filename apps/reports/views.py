# ==============================================================================
# 12. APP: REPORTS (Views)
# Archivo destino: apps/reports/views.py
# ==============================================================================
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Sum, F
from apps.products.models import Inventory
from apps.sales.models import Sale
from apps.users.permissions import IsGerenteOrHigher
from django.utils.dateparse import parse_date

class StockReportView(APIView):
    """
    Requisito PDF: Reporte de stock por sucursal.
    GET /api/reports/stock/?branch=ID
    """
    permission_classes = [IsAuthenticated, IsGerenteOrHigher]

    def get(self, request):
        user_company = request.user.company
        branch_id = request.query_params.get('branch')
        
        queryset = Inventory.objects.filter(branch__company=user_company)
        
        if branch_id:
            queryset = queryset.filter(branch_id=branch_id)
            
        data = queryset.values(
            'branch__name', 
            'product__name', 
            'stock',
            valor_inventario=F('stock') * F('product__cost')
        )
        return Response(data)

class SalesReportView(APIView):
    """
    Requisito PDF: Reporte de ventas por periodo (dia/mes) por sucursal.
    GET /api/reports/sales/?branch=ID&date_from=YYYY-MM-DD&date_to=YYYY-MM-DD
    """
    permission_classes = [IsAuthenticated, IsGerenteOrHigher]
    
    def get(self, request):
        user_company = request.user.company
        branch_id = request.query_params.get('branch')
        date_from = request.query_params.get('date_from')
        date_to = request.query_params.get('date_to')

        queryset = Sale.objects.filter(branch__company=user_company)

        if branch_id:
            queryset = queryset.filter(branch_id=branch_id)
        if date_from:
            queryset = queryset.filter(created_at__date__gte=parse_date(date_from))
        if date_to:
            queryset = queryset.filter(created_at__date__lte=parse_date(date_to))

        # Resumen totalizado
        total_sales = queryset.aggregate(Sum('total'))['total__sum'] or 0
        count_sales = queryset.count()
        
        return Response({
            'total_sales': total_sales,
            'count_sales': count_sales,
            'period': f"{date_from} to {date_to}"
        })