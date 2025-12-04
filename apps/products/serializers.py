from rest_framework import serializers  
from .models import Product, Inventory, Branch, Supplier  
from apps.users.models import Company  
from utils.validators import validar_rut  

# Serializador para el modelo 'Branch' (Sucursal)
class BranchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Branch  # Especifica que este serializador se utiliza para el modelo 'Branch'
        fields = '__all__'  # Incluye todos los campos del modelo en el serializador

    # Método sobrescrito para personalizar la creación de un objeto Branch
    def create(self, validated_data):
        user = self.context['request'].user  # Obtiene el usuario que está realizando la solicitud
        # Si el usuario tiene asociada una empresa, asignamos automáticamente esa empresa a la sucursal
        if user.company:
            validated_data['company'] = user.company
        # Si el usuario es Super Admin y no envió la empresa, el modelo o la validación fallarán
        return super().create(validated_data)

# Serializador para el modelo 'Supplier' (Proveedor)
class SupplierSerializer(serializers.ModelSerializer):
    rut = serializers.CharField(validators=[validar_rut])  # Valida el RUT del proveedor usando el validador 'validar_rut'
    company = serializers.PrimaryKeyRelatedField(queryset=Company.objects.all(), required=False)  # Relaciona con el modelo Company, el campo es opcional

    class Meta:
        model = Supplier  # Especifica que este serializador se utiliza para el modelo 'Supplier'
        fields = '__all__'  # Incluye todos los campos del modelo en el serializador

    # Método sobrescrito para personalizar la creación de un objeto Supplier
    def create(self, validated_data):
        user = self.context['request'].user  # Obtiene el usuario que está realizando la solicitud
        
        # REGLA DE ORO:
        # 1. Si el usuario tiene asignada una empresa (empleado), el sistema usa esa empresa para el proveedor, ignorando lo que envíe el cliente
        if user.company:
            validated_data['company'] = user.company
        
        # 2. Si el usuario es Super Admin (sin empresa asignada), debe enviar explícitamente el campo 'company'
        elif not validated_data.get('company'):
            # Si el Super Admin no envía 'company', se lanza un error indicando que debe seleccionar una empresa
            raise serializers.ValidationError({"company": "Como Super Admin, debe seleccionar una empresa para este registro."})
        
        return super().create(validated_data)

# Serializador para el modelo 'Product' (Producto)
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product  # Especifica que este serializador se utiliza para el modelo 'Product'
        fields = '__all__'  # Incluye todos los campos del modelo en el serializador

    # Método sobrescrito para personalizar la creación de un objeto Product
    def create(self, validated_data):
        user = self.context['request'].user  # Obtiene el usuario que está realizando la solicitud
        # Si el usuario tiene asociada una empresa, asignamos automáticamente esa empresa al producto
        if user.company:
            validated_data['company'] = user.company
        return super().create(validated_data)

# Serializador para el modelo 'Inventory' (Inventario)
class InventorySerializer(serializers.ModelSerializer):
    # Campos adicionales para mostrar información de nombre de producto, nombre de sucursal y SKU
    product_name = serializers.CharField(source='product.name', read_only=True)  # Nombre del producto, solo lectura
    branch_nam_
