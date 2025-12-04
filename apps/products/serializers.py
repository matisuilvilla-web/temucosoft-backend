from rest_framework import serializers
from .models import Product, Inventory, Branch, Supplier
from apps.users.models import Company
from utils.validators import validar_rut

# Requisito PDF: CRUD de Branches (Sucursales)
class BranchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Branch
        fields = '__all__'
       

    def create(self, validated_data):
        user = self.context['request'].user
        # Si el usuario tiene empresa, forzamos esa.
        if user.company:
            validated_data['company'] = user.company
        # Si es Super Admin y no mandó empresa, fallará a nivel de modelo o validación previa
        return super().create(validated_data)

class SupplierSerializer(serializers.ModelSerializer):
    rut = serializers.CharField(validators=[validar_rut])
    company = serializers.PrimaryKeyRelatedField(queryset=Company.objects.all(), required=False)

    class Meta:
        model = Supplier
        fields = '__all__'

    def create(self, validated_data):
        user = self.context['request'].user
        
        # REGLA DE ORO:
        # 1. Si es empleado (tiene company), el sistema IMPONE su empresa. Ignora lo que envíe.
        if user.company:
            validated_data['company'] = user.company
        
        # 2. Si es Super Admin (no tiene company), DEBE haber enviado el campo 'company'.
        # Si no lo envió, lanzamos error limpio.
        elif not validated_data.get('company'):
             raise serializers.ValidationError({"company": "Como Super Admin, debe seleccionar una empresa para este registro."})
             
        return super().create(validated_data)

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

    def create(self, validated_data):
        user = self.context['request'].user
        if user.company:
            validated_data['company'] = user.company
        return super().create(validated_data)

class InventorySerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)
    branch_name = serializers.CharField(source='branch.name', read_only=True)
    sku = serializers.CharField(source='product.sku', read_only=True)

    class Meta:
        model = Inventory
        fields = '__all__'