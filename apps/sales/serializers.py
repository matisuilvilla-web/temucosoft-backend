class SaleDetailSerializer(serializers.ModelSerializer):
    product_sku = serializers.CharField(source='product.sku', read_only=True)  # SKU del producto, solo lectura
    product_name = serializers.CharField(source='product.name', read_only=True)  # Nombre del producto, solo lectura
    quantity = serializers.IntegerField(validators=[validar_cantidad_minima])  # Valida la cantidad mínima permitida
    
    class Meta:
        model = SaleDetail
        fields = ('id', 'product', 'product_sku', 'product_name', 'quantity', 'price_at_moment')
        extra_kwargs = {'price_at_moment': {'read_only': True}}  # El precio se toma del producto, no es editable

class SaleSerializer(serializers.ModelSerializer):
    items = SaleDetailSerializer(many=True)  # Define un serializador anidado para los detalles de la venta (productos)
    vendedor_name = serializers.CharField(source='user.username', read_only=True)  # Nombre del vendedor, solo lectura

    class Meta:
        model = Sale
        fields = ('id', 'branch', 'user', 'vendedor_name', 'total', 'payment_method', 'created_at', 'items')
        read_only_fields = ('total', 'user', 'created_at')  # Los campos 'total', 'user' y 'created_at' son solo lectura

    def create(self, validated_data):
        items_data = validated_data.pop('items')  # Extrae los datos de los productos de la venta
        branch = validated_data.get('branch')  # Obtiene la sucursal de la venta
        
        # Transacción atómica para garantizar que la venta y el inventario se actualicen de forma segura
        with transaction.atomic():
            # 1. Crear la venta
            sale = Sale.objects.create(**validated_data)  # Crea el objeto 'Sale' con los datos validados
            total_amount = 0  # Inicializa el monto total de la venta

            for item in items_data:  # Itera sobre los productos vendidos
                product = item['product']  # Producto de la venta
                quantity = item['quantity']  # Cantidad de ese producto en la venta
                
                # 2. Validar que haya stock disponible en la sucursal
                try:
                    inventory = Inventory.objects.get(branch=branch, product=product)  # Busca el inventario de ese producto en la sucursal
                except Inventory.DoesNotExist:
                    raise serializers.ValidationError(f"El producto {product.name} no tiene inventario inicializado en esta sucursal.")  # Si no existe el inventario, lanza error

                if inventory.stock < quantity:  # Si el stock es insuficiente
                    raise serializers.ValidationError(f"Stock insuficiente para {product.name}. Disponible: {inventory.stock}")

                # 3. Descontar el stock
                inventory.stock -= quantity  # Reduce la cantidad en inventario
                inventory.save()  # Guarda la actualización del inventario

                # 4. Crear el detalle de la venta
                price = product.price  # Obtiene el precio del producto
                SaleDetail.objects.create(
                    sale=sale,
                    product=product,
                    quantity=quantity,
                    price_at_moment=price  # Guarda el precio al momento de la venta
                )
                total_amount += (price * quantity)  # Suma el total de la venta por el producto

            # 5. Actualizar el total de la venta
            sale.total = total_amount  # Asigna el total calculado
            sale.save()  # Guarda la venta con el total actualizado
            
        return sale  # Devuelve la venta creada
