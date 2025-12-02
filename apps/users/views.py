# ==============================================================================
# 8. APP: USERS (Vistas de Auth y Gestión)
# Archivo destino: apps/users/views.py
# ==============================================================================
from rest_framework import viewsets, generics, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView
from .models import User, Company, Subscription
from .serializers import UserSerializer, CompanySerializer, MyTokenObtainPairSerializer
from .permissions import IsSuperAdmin, IsAdminCliente

# Vista de Login Personalizada
class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

# Vista de Registro (Opcional, para clientes nuevos)
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = UserSerializer

# Gestión de Compañías (Solo SuperAdmin)
class CompanyViewSet(viewsets.ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    permission_classes = [IsAuthenticated, IsSuperAdmin]

    @action(detail=True, methods=['post'])
    def subscribe(self, request, pk=None):
        """Endpoint para activar plan: POST /api/companies/{id}/subscribe/"""
        company = self.get_object()
        plan_name = request.data.get('plan_name', 'BASIC')
        start_date = request.data.get('start_date')
        end_date = request.data.get('end_date')
        
        # Crear o actualizar suscripción
        Subscription.objects.update_or_create(
            company=company,
            defaults={
                'plan_name': plan_name,
                'start_date': start_date,
                'end_date': end_date,
                'is_active': True
            }
        )
        return Response({'status': f'Suscripción {plan_name} actualizada correctamente'})

# Gestión de Usuarios
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'SUPER_ADMIN':
            return User.objects.all()
        # Admin Cliente ve solo sus empleados
        if user.role == 'ADMIN_CLIENTE':
            return User.objects.filter(company=user.company)
        # Usuarios normales solo se ven a sí mismos
        return User.objects.filter(id=user.id)

    @action(detail=False, methods=['get'])
    def me(self, request):
        """Endpoint para obtener datos del usuario actual: GET /api/users/me/"""
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)