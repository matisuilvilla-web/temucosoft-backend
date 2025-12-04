from .models import User, Company, Subscription 
from .serializers import UserSerializer, CompanySerializer, MyTokenObtainPairSerializer  
from .permissions import IsSuperAdmin, IsAdminCliente  

# Vista de Login Personalizada (JWT)
class MyTokenObtainPairView(TokenObtainPairView):
    """Vista personalizada para obtener el token JWT"""
    serializer_class = MyTokenObtainPairSerializer  # Utiliza el serializador personalizado para agregar información extra al token

# Vista de Registro (Opcional, para clientes nuevos)
class RegisterView(generics.CreateAPIView):
    """Vista para registrar un nuevo usuario"""
    queryset = User.objects.all()  # Consultas para obtener todos los usuarios
    permission_classes = (AllowAny,)  # Permite el acceso a cualquier usuario (sin autenticación)
    serializer_class = UserSerializer  # Utiliza el serializador de usuarios para crear un nuevo usuario

# Gestión de Compañías (Solo SuperAdmin puede acceder)
class CompanyViewSet(viewsets.ModelViewSet):
    """Vista para gestionar las compañías, solo accesible por SuperAdmin"""
    queryset = Company.objects.all()  # Devuelve todas las compañías
    serializer_class = CompanySerializer  # Utiliza el serializador de compañías
    permission_classes = [IsAuthenticated, IsSuperAdmin]  # Solo usuarios autenticados con rol 'SUPER_ADMIN' pueden acceder

    @action(detail=True, methods=['post'])
    def subscribe(self, request, pk=None):
        """Endpoint para activar la suscripción de una compañía: POST /api/companies/{id}/subscribe/"""
        company = self.get_object()  # Obtiene la compañía seleccionada (usando 'id' desde la URL)
        plan_name = request.data.get('plan_name', 'BASIC')  # Obtiene el plan de suscripción (por defecto 'BASIC')
        start_date = request.data.get('start_date')  # Fecha de inicio de la suscripción
        end_date = request.data.get('end_date')  # Fecha de fin de la suscripción
        
        # Crear o actualizar la suscripción para la compañía
        Subscription.objects.update_or_create(
            company=company,  # Relaciona la suscripción con la compañía
            defaults={
                'plan_name': plan_name,
                'start_date': start_date,
                'end_date': end_date,
                'is_active': True  # Marca la suscripción como activa
            }
        )
        return Response({'status': f'Suscripción {plan_name} actualizada correctamente'})  # Responde con el estado de la operación

# Gestión de Usuarios
class UserViewSet(viewsets.ModelViewSet):
    """Vista para gestionar usuarios"""
    queryset = User.objects.all()  # Devuelve todos los usuarios
    serializer_class = UserSerializer  # Utiliza el serializador de usuarios
    permission_classes = [IsAuthenticated]  # Solo usuarios autenticados pueden acceder

    def get_queryset(self):
        """Filtra la consulta de usuarios según el rol"""
        user = self.request.user
        if user.role == 'SUPER_ADMIN':
            return User.objects.all()  # El Super Admin puede ver todos los usuarios
        if user.role == 'ADMIN_CLIENTE':
            return User.objects.filter(company=user.company)  # El Admin Cliente solo puede ver los usuarios de su empresa
        return User.objects.filter(id=user.id)  # Los usuarios normales solo pueden ver su propia información

    @action(detail=False, methods=['get'])
    def me(self, request):
        """Endpoint para obtener los datos del usuario autenticado: GET /api/users/me/"""
        serializer = self.get_serializer(request.user)  # Serializa los datos del usuario autenticado
        return Response(serializer.data)  # Devuelve la respuesta con los datos del usuario
