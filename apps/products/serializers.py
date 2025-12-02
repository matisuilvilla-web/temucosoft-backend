from rest_framework import serializers
from .models import Product, Inventory, Branch, Supplier
from utils.validators import validar_rut

# Requisito PDF: CRUD de Branches (Sucursales)
class BranchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Branch
        fields = '__all__'
        read_only_fields = ('company',) # Usuario no elige la compañía, se asigna sola

    def create(self, validated_data):
        # Asignar automáticamente la compañía del usuario creador
        user = self.context['request'].user
        validated_data['company'] = user.company
        return super().create(validated_data)

# Requisito PDF: CRUD de Suppliers (Proveedores)
class SupplierSerializer(serializers.ModelSerializer):
    rut = serializers.CharField(validators=[validar_rut])

    class Meta:
        model = Supplier
        fields = '__all__'
        read_only_fields = ('company',) # Importante: read_only

    def create(self, validated_data):
        # Asignar automáticamente la compañía del usuario creador
        user = self.context['request'].user
        validated_data['company'] = user.company
        return super().create(validated_data)

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'
        read_only_fields = ('company',) 

    def create(self, validated_data):
        user = self.context['request'].user
        validated_data['company'] = user.company
        return super().create(validated_data)

class InventorySerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)
    branch_name = serializers.CharField(source='branch.name', read_only=True)
    sku = serializers.CharField(source='product.sku', read_only=True)

    class Meta:
        model = Inventory
        fields = '__all__'