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
    Reporte de stock por sucursal.
    GET /api/reports/stock/?branch=ID
    """
    permission_classes = [IsAuthenticated, IsGerenteOrHigher]

    def get(self, request):
        user_company = request.user.company
        branch_id = request.query_params.get('branch')

        # Filtra inventario solo para la empresa del usuario
        queryset = Inventory.objects.filter(branch__company=user_company)
        
        # Filtra por sucursal si se especifica 'branch'
        if branch_id:
            queryset = queryset.filter(branch_id=branch_id)
        
        # Obtiene datos del inventario con el nombre de la sucursal, nombre del producto, stock y valor calculado
        data = queryset.values(
            'branch__name',  # Nombre de la sucursal
            'product__name',  # Nombre del producto
            'stock',  # Cantidad en stock
            valor_inventario=F('stock') * F('product__cost')  # Calcula valor total del inventario
        )
        
        return Response(data)

class SalesReportView(APIView):
    """
    Reporte de ventas por periodo y sucursal.
    GET /api/reports/sales/?branch=ID&date_from=YYYY-MM-DD&date_to=YYYY-MM-DD
    """
    permission_classes = [IsAuthenticated, IsGerenteOrHigher]
    
    def get(self, request):
        user_company = request.user.company
        branch_id = request.query_params.get('branch')
        date_from = request.query_params.get('date_from')
        date_to = request.query_params.get('date_to')

        # Filtra ventas solo para la empresa del usuario
        queryset = Sale.objects.filter(branch__company=user_company)

        # Filtra por sucursal si se especifica 'branch'
        if branch_id:
            queryset = queryset.filter(branch_id=branch_id)
        
        # Filtra por fechas si se especifica 'date_from' y 'date_to'
        if date_from:
            queryset = queryset.filter(created_at__date__gte=parse_date(date_from))
        if date_to:
            queryset = queryset.filter(created_at__date__lte=parse_date(date_to))

        # Agrega resumen de ventas: total y cantidad de ventas
        total_sales = queryset.aggregate(Sum('total'))['total__sum'] or 0
        count_sales = queryset.count()
        
        return Response({
            'total_sales': total_sales,  # Total de ventas en el periodo
            'count_sales': count_sales,  # Número de ventas en el periodo
            'period': f"{date_from} to {date_to}"  # Periodo de fechas solicitado
        })
