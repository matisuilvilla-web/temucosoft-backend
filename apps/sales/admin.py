from django.contrib import admin
from .models import Sale, SaleDetail

class SaleDetailInline(admin.TabularInline):
    model = SaleDetail
    extra = 0

@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):
    list_display = ('id', 'created_at', 'total', 'payment_method', 'branch', 'user')
    inlines = [SaleDetailInline]