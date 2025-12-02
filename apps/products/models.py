# ==============================================================================
# 4. APP: PRODUCTS (Modelos)
# Archivo destino: apps/products/models.py
# ==============================================================================
from django.db import models
from apps.users.models import Company
from utils.validators import validar_rut, validar_positivo

class Supplier(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE) # Multi-tenancy
    name = models.CharField(max_length=100)
    rut = models.CharField(max_length=20, validators=[validar_rut])
    contact_email = models.EmailField()
    phone = models.CharField(max_length=20)

    def __str__(self):
        return self.name

class Branch(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=200)
    phone = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.name} - {self.company.name}"

class Product(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    sku = models.CharField(max_length=50)
    name = models.CharField(max_length=150)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[validar_positivo])
    cost = models.DecimalField(max_digits=10, decimal_places=2, validators=[validar_positivo])
    category = models.CharField(max_length=50)

    class Meta:
        unique_together = ('company', 'sku')

    def __str__(self):
        return self.name

class Inventory(models.Model):
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, related_name='inventory')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='stock_records')
    stock = models.IntegerField(default=0, validators=[validar_positivo])
    reorder_point = models.IntegerField(default=5)

    class Meta:
        unique_together = ('branch', 'product')
    
    def __str__(self):
        return f"{self.product.name} @ {self.branch.name}: {self.stock}"