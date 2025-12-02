from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    
    # Operaciones
    path('pos/', views.pos_view, name='pos'),
    path('inventory/', views.inventory_view, name='inventory'),
    path('suppliers/', views.suppliers_view, name='suppliers'),
    path('purchases/', views.purchases_view, name='purchases'),
    path('reports/sales/', views.sales_report_view, name='sales-report'),
    
    # Gestión Administrativa
    path('manage/users/', views.users_manage_view, name='manage-users'),
    path('manage/companies/', views.companies_manage_view, name='manage-companies'),

    # Shop
    path('shop/', views.shop_catalogue_view, name='shop-catalogue'),
    path('shop/cart/', views.shop_cart_view, name='shop-cart'),
]