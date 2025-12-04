from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer  
from .models import User, Company, Subscription  
from utils.validators import validar_rut  

# Serializador para la Empresa (Company)
class CompanySerializer(serializers.ModelSerializer):
    rut = serializers.CharField(validators=[validar_rut])  # Valida el RUT de la empresa usando un validador personalizado

    class Meta:
        model = Company
        fields = '__all__'  # Incluir todos los campos del modelo Company

# Serializador para la Suscripción (Subscription)
class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = '__all__'  # Incluir todos los campos del modelo Subscription

    def validate(self, data):
        """Validación estricta de fechas"""
        # Valida que la fecha de fin no sea anterior o igual a la fecha de inicio
        if data['end_date'] <= data['start_date']:
            raise serializers.ValidationError("La fecha de término debe ser posterior a la de inicio.")
        return data

# Serializador para el Usuario (User)
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'rut', 'role', 'company', 'password')
        extra_kwargs = {'password': {'write_only': True}}  # El campo 'password' solo es escribible
        read_only_fields = ('company',)  # El campo 'company' es solo lectura (no se puede modificar directamente)

    def create(self, validated_data):
        """Asignación inteligente de empresa al crear el usuario"""
        request = self.context.get('request')  # Obtiene la solicitud actual
        if request and request.user.is_authenticated:
            # Si el usuario está autenticado y es un Admin Cliente, asigna su empresa al nuevo usuario
            if request.user.company:
                validated_data['company'] = request.user.company
        
        # Si es Super Admin y no se especifica empresa, 'company' será None
        # Crea el usuario con los datos validados (incluyendo la empresa, si es un Admin Cliente)
        user = User.objects.create_user(**validated_data)
        return user

# Serializador para personalizar el token JWT
class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    """Personaliza el token JWT para incluir rol y compañía"""
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)  # Llama a la implementación base para generar el token
        # Agrega información personalizada al token
        token['role'] = user.role  # Añade el rol del usuario al token
        token['username'] = user.username  # Añade el nombre de usuario al token
        if user.company:
            token['company_id'] = user.company.id  # Si el usuario tiene una empresa asociada, incluye el ID de la empresa
        return token
