from django.shortcuts import render

def login_view(request):
    return render(request, 'login.html')

def dashboard_view(request):
    return render(request, 'dashboard.html')

# Módulos Operativos
def pos_view(request):
    return render(request, 'pos.html')

def inventory_view(request):
    return render(request, 'inventory.html')

def suppliers_view(request):
    return render(request, 'suppliers.html')

def purchases_view(request):
    return render(request, 'purchases.html')

def sales_report_view(request):
    return render(request, 'sales_report.html')

# E-commerce
def shop_catalogue_view(request):
    return render(request, 'shop_catalogue.html')

def shop_cart_view(request):
    return render(request, 'shop_cart.html')

# --- NUEVAS VISTAS DE GESTIÓN (REQUISITO PDF) ---
def users_manage_view(request):
    """Gestión de Usuarios (Solo Admin Cliente)"""
    return render(request, 'users_manage.html')

def companies_manage_view(request):
    """Gestión de Empresas/Tenants (Solo Super Admin)"""
    return render(request, 'companies_manage.html')