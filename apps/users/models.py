# ==============================================================================
# 2. APP: USERS (Modelos y Permisos)
# Archivo destino: apps/users/models.py
# ==============================================================================
from django.db import models
from django.contrib.auth.models import AbstractUser
from utils.validators import validar_rut

class Company(models.Model):
    """Representa al Cliente/Tenant (La Pyme que contrata el software)"""
    name = models.CharField(max_length=100)
    rut = models.CharField(max_length=20, validators=[validar_rut])
    address = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Subscription(models.Model):
    PLAN_CHOICES = (
        ('BASIC', 'Básico'),
        ('STANDARD', 'Estándar'),
        ('PREMIUM', 'Premium'),
    )
    company = models.OneToOneField(Company, on_delete=models.CASCADE, related_name='subscription')
    plan_name = models.CharField(max_length=20, choices=PLAN_CHOICES, default='BASIC')
    start_date = models.DateField()
    end_date = models.DateField()
    is_active = models.BooleanField(default=True)

class User(AbstractUser):
    """Usuario personalizado que soporta Roles y RUT"""
    ROLE_CHOICES = (
        ('SUPER_ADMIN', 'Super Admin (TemucoSoft)'),
        ('ADMIN_CLIENTE', 'Administrador Cliente (Dueño)'),
        ('GERENTE', 'Gerente'),
        ('VENDEDOR', 'Vendedor'),
        ('CLIENTE_FINAL', 'Cliente Final (E-commerce)'),
    )
    
    rut = models.CharField(max_length=20, validators=[validar_rut], blank=True, null=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='CLIENTE_FINAL')
    company = models.ForeignKey(Company, on_delete=models.SET_NULL, null=True, blank=True, related_name='users')
    
    # Requisito: is_active debe verificarse (Django lo hace por defecto, pero lo agregamos explícito si es necesario)