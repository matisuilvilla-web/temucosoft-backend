from django.contrib import admin
from .models import User, Company, Subscription

@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('name', 'rut', 'created_at')

@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('company', 'plan_name', 'is_active', 'end_date')

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'role', 'company', 'rut')
    list_filter = ('role', 'company')