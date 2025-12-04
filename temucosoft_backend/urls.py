from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView
from apps.users.views import UserViewSet, CompanyViewSet, MyTokenObtainPairView, RegisterView
from apps.products.views import ProductViewSet, InventoryViewSet, SupplierViewSet, BranchViewSet
from apps.sales.views import SaleViewSet
from apps.reports.views import StockReportView, SalesReportView

# Router Principal
router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'companies', CompanyViewSet)
router.register(r'products', ProductViewSet, basename='product')
router.register(r'inventory', InventoryViewSet, basename='inventory')
router.register(r'suppliers', SupplierViewSet, basename='supplier')
router.register(r'branches', BranchViewSet, basename='branch')
router.register(r'sales', SaleViewSet, basename='sale') # CRUD de Ventas POS

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Auth JWT
    path('api/token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/register/', RegisterView.as_view(), name='register'),
    
    # API Router (CRUDs automáticos)
    path('api/', include(router.urls)),
    
    # Reportes Manuales (endpoints específicos)
    path('api/reports/stock/', StockReportView.as_view(), name='report-stock'),
    path('api/reports/sales/', SalesReportView.as_view(), name='report-sales'),

    # --- FRONTEND (WEB) ---
    path('', include('apps.web.urls')), # Conectamos la app web a la raíz
]
