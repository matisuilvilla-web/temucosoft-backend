# ==============================================================================
# 10. APP: SALES (Serializers - LÓGICA COMPLEJA AQUÍ)
# Archivo destino: apps/sales/serializers.py
# ==============================================================================
from rest_framework import serializers
from django.db import transaction
from utils.validators import validar_cantidad_minima
from .models import Sale, SaleDetail
from apps.products.models import Product, Inventory

class SaleDetailSerializer(serializers.ModelSerializer):
    product_sku = serializers.CharField(source='product.sku', read_only=True)
    product_name = serializers.CharField(source='product.name', read_only=True)
    quantity = serializers.IntegerField(validators=[validar_cantidad_minima])
    
    class Meta:
        model = SaleDetail
        fields = ('id', 'product', 'product_sku', 'product_name', 'quantity', 'price_at_moment')
        extra_kwargs = {'price_at_moment': {'read_only': True}} # Se toma del producto

class SaleSerializer(serializers.ModelSerializer):
    items = SaleDetailSerializer(many=True) # Nested Serializer para recibir items en el JSON
    vendedor_name = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = Sale
        fields = ('id', 'branch', 'user', 'vendedor_name', 'total', 'payment_method', 'created_at', 'items')
        read_only_fields = ('total', 'user', 'created_at')

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        branch = validated_data.get('branch')
        
        # Requisito PDF: Validación de Stock y Transacción Atómica
        # Si falla algo, no se crea la venta ni se descuenta stock a medias.
        with transaction.atomic():
            # 1. Crear Venta
            sale = Sale.objects.create(**validated_data)
            total_amount = 0

            for item in items_data:
                product = item['product']
                quantity = item['quantity']
                
                # Validar Stock
                try:
                    inventory = Inventory.objects.get(branch=branch, product=product)
                except Inventory.DoesNotExist:
                    raise serializers.ValidationError(f"El producto {product.name} no tiene inventario inicializado en esta sucursal.")

                if inventory.stock < quantity:
                    raise serializers.ValidationError(f"Stock insuficiente para {product.name}. Disponible: {inventory.stock}")

                # Descontar Stock
                inventory.stock -= quantity
                inventory.save()

                # Crear Detalle
                price = product.price
                SaleDetail.objects.create(
                    sale=sale,
                    product=product,
                    quantity=quantity,
                    price_at_moment=price
                )
                total_amount += (price * quantity)

            # Actualizar total de la venta
            sale.total = total_amount
            sale.save()
            
        return sale