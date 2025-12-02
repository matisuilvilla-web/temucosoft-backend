from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import User, Company, Subscription
from utils.validators import validar_rut

class CompanySerializer(serializers.ModelSerializer):
    rut = serializers.CharField(validators=[validar_rut])
    class Meta:
        model = Company
        fields = '__all__'

class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = '__all__'

    def validate(self, data):
        """Validación estricta de fechas"""
        if data['end_date'] <= data['start_date']:
            raise serializers.ValidationError("La fecha de término debe ser posterior a la de inicio.")
        return data
    
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'rut', 'role', 'company', 'password')
        extra_kwargs = {'password': {'write_only': True}}
        read_only_fields = ('company',)

    def create(self, validated_data):
        # Lógica inteligente de asignación de empresa
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            # Si soy Admin Cliente, el usuario que creo es de mi empresa
            if request.user.company:
                validated_data['company'] = request.user.company
        
        # Nota: Si es Super Admin creando usuarios sin compañía, user.company será None y no entra al if, lo cual es correcto.
        
        user = User.objects.create_user(**validated_data)
        return user

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    """Personaliza el token JWT para incluir rol y compañía"""
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # Add custom claims
        token['role'] = user.role
        token['username'] = user.username
        if user.company:
            token['company_id'] = user.company.id
        return token