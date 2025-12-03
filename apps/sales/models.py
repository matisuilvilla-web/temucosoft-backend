from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError
from apps.users.models import User
from apps.products.models import Branch, Product

def validar_fecha_no_futura(value):
    if value > timezone.now():
        raise ValidationError("La fecha no puede estar en el futuro.")

class Sale(models.Model):
    """Venta POS"""
    PAYMENT_METHODS = (('CASH', 'Efectivo'), ('CARD', 'Tarjeta'), ('TRANSFER', 'Transferencia'))
    
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True) # Vendedor
    total = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHODS)
    created_at = models.DateTimeField(default=timezone.now, validators=[validar_fecha_no_futura])

class SaleDetail(models.Model):
    sale = models.ForeignKey(Sale, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    quantity = models.PositiveIntegerField()
    price_at_moment = models.DecimalField(max_digits=10, decimal_places=2)

    def save(self, *args, **kwargs):
        # Lógica simple para descontar inventario podría ir aquí o en el Serializer (recomendado en Serializer)
        super().save(*args, **kwargs)

class Order(models.Model):
    """E-commerce Order"""
    STATUS_CHOICES = (('PENDING', 'Pendiente'), ('SHIPPED', 'Enviado'), ('DELIVERED', 'Entregado'))
    
    client_name = models.CharField(max_length=100) # Cliente final no registrado
    client_email = models.EmailField()
    total = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    created_at = models.DateTimeField(auto_now_add=True)