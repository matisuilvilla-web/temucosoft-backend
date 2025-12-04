from django.shortcuts import render  

# Vista de Login
def login_view(request):
    """Vista para el formulario de inicio de sesión"""
    return render(request, 'login.html')  # Renderiza la plantilla 'login.html'

# Vista de Dashboard
def dashboard_view(request):
    """Vista para el panel principal del usuario (Dashboard)"""
    return render(request, 'dashboard.html')  # Renderiza la plantilla 'dashboard.html'

# Módulos Operativos
def pos_view(request):
    """Vista para la interfaz del punto de venta (POS)"""
    return render(request, 'pos.html')  # Renderiza la plantilla 'pos.html'

def inventory_view(request):
    """Vista para la gestión del inventario"""
    return render(request, 'inventory.html')  # Renderiza la plantilla 'inventory.html'

def suppliers_view(request):
    """Vista para la gestión de proveedores"""
    return render(request, 'suppliers.html')  # Renderiza la plantilla 'suppliers.html'

def purchases_view(request):
    """Vista para la gestión de compras"""
    return render(request, 'purchases.html')  # Renderiza la plantilla 'purchases.html'

def sales_report_view(request):
    """Vista para generar el reporte de ventas"""
    return render(request, 'sales_report.html')  # Renderiza la plantilla 'sales_report.html'

# E-commerce
def shop_catalogue_view(request):
    """Vista para el catálogo de productos en la tienda online"""
    return render(request, 'shop_catalogue.html')  # Renderiza la plantilla 'shop_catalogue.html'

def shop_cart_view(request):
    """Vista para el carrito de compras"""
    return render(request, 'shop_cart.html')  # Renderiza la plantilla 'shop_cart.html'

def users_manage_view(request):
    """Gestión de Usuarios (Solo Admin Cliente)"""
    # Esta vista es solo accesible por el rol 'Admin Cliente' (puede agregarse validación de permisos si es necesario)
    return render(request, 'users_manage.html')  # Renderiza la plantilla 'users_manage.html'

def companies_manage_view(request):
    """Gestión de Empresas/Tenants (Solo Super Admin)"""
    # Esta vista es solo accesible por el rol 'Super Admin' (también podría requerir validación de permisos)
    return render(request, 'companies_manage.html')  # Renderiza la plantilla 'companies_manage.html'
