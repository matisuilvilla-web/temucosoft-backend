from django.db import models
from django.contrib.auth.models import AbstractUser  
from utils.validators import validar_rut  

# Modelo de Empresa (Cliente/Tenant)
class Company(models.Model):
    """Representa al Cliente/Tenant (La Pyme que contrata el software)"""
    name = models.CharField(max_length=100)  # Nombre de la empresa
    rut = models.CharField(max_length=20, validators=[validar_rut])  # RUT de la empresa, validado con una función personalizada
    address = models.CharField(max_length=200)  # Dirección de la empresa
    created_at = models.DateTimeField(auto_now_add=True)  # Fecha de creación de la empresa
    
    def __str__(self):
        return self.name  # Devuelve el nombre de la empresa como representación en texto

# Modelo de Suscripción
class Subscription(models.Model):
    PLAN_CHOICES = (
        ('BASIC', 'Básico'),
        ('STANDARD', 'Estándar'),
        ('PREMIUM', 'Premium'),
    )
    
    company = models.OneToOneField(Company, on_delete=models.CASCADE, related_name='subscription')  # Relación con la empresa
    plan_name = models.CharField(max_length=20, choices=PLAN_CHOICES, default='BASIC')  # Plan de suscripción (Básico, Estándar o Premium)
    start_date = models.DateField()  # Fecha de inicio de la suscripción
    end_date = models.DateField()  # Fecha de fin de la suscripción
    is_active = models.BooleanField(default=True)  # Estado de la suscripción (activa o no)

# Usuario personalizado con soporte de Roles y RUT
class User(AbstractUser):
    """Usuario personalizado que soporta Roles y RUT"""
    ROLE_CHOICES = (
        ('SUPER_ADMIN', 'Super Admin (TemucoSoft)'),
        ('ADMIN_CLIENTE', 'Administrador Cliente (Dueño)'),
        ('GERENTE', 'Gerente'),
        ('VENDEDOR', 'Vendedor'),
        ('CLIENTE_FINAL', 'Cliente Final (E-commerce)'),
    )
    
    rut = models.CharField(max_length=20, validators=[validar_rut], blank=True, null=True)  # RUT del usuario, validado con la misma función
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='CLIENTE_FINAL')  # Rol del usuario (como Super Admin, Gerente, etc.)
    company = models.ForeignKey(Company, on_delete=models.SET_NULL, null=True, blank=True, related_name='users')  # Relación con la empresa (opcional, puede ser null)
