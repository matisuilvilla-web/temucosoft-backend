from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError
from apps.users.models import User  
from apps.products.models import Branch, Product  

# Validador personalizado para asegurar que la fecha no sea futura
def validar_fecha_no_futura(value):
    if value > timezone.now():
        raise ValidationError("La fecha no puede estar en el futuro.")

# Modelo de Venta (POS)
class Sale(models.Model):
    """Venta POS"""
    PAYMENT_METHODS = (('CASH', 'Efectivo'), ('CARD', 'Tarjeta'), ('TRANSFER', 'Transferencia'))
    
    # Relación con la sucursal y el vendedor
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)  # Vendedor de la venta
    
    # Información de la venta
    total = models.DecimalField(max_digits=12, decimal_places=2, default=0)  # Total de la venta
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHODS)  # Método de pago
    created_at = models.DateTimeField(default=timezone.now, validators=[validar_fecha_no_futura])  # Fecha de creación, no puede ser futura

# Detalle de la venta
class SaleDetail(models.Model):
    sale = models.ForeignKey(Sale, on_delete=models.CASCADE, related_name='items')  # Relacionado con la venta principal
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)  # Relacionado con el producto vendido
    quantity = models.PositiveIntegerField()  # Cantidad vendida
    price_at_moment = models.DecimalField(max_digits=10, decimal_places=2)  # Precio del producto en el momento de la venta

    def save(self, *args, **kwargs):
        # Lógica para descontar inventario puede ser añadida aquí o en el serializador (mejor en el serializador)
        super().save(*args, **kwargs)

# Modelo de Pedido para E-commerce
class Order(models.Model):
    """E-commerce Order"""
    STATUS_CHOICES = (('PENDING', 'Pendiente'), ('SHIPPED', 'Enviado'), ('DELIVERED', 'Entregado'))  # Estado del pedido
    
    # Información del cliente (cliente final no registrado)
    client_name = models.CharField(max_length=100)  # Nombre del cliente
    client_email = models.EmailField()  # Correo electrónico del cliente
    total = models.DecimalField(max_digits=12, decimal_places=2, default=0)  # Total del pedido
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')  # Estado del pedido
    created_at = models.DateTimeField(auto_now_add=True)  # Fecha de creación del pedido
