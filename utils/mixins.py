class MultiTenantModelMixin:
    """
    Mixin mágico para filtrar datos por empresa automáticamente.
    - Super Admin -> Ve TODO.
    - Usuario con Company -> Ve solo SU company.
    - Usuario sin Company (y no super admin) -> No ve nada.
    """
    def get_queryset(self):
        # 1. Obtenemos el queryset base del modelo (ej: Product.objects.all())
        qs = super().get_queryset()
        
        user = self.request.user
        
        # 2. Si es Super Admin, retornamos todo sin filtrar
        if user.role == 'SUPER_ADMIN':
            return qs
        
        # 3. Si es usuario de empresa, filtramos por su empresa
        if user.company:
            # Nota: Asumimos que el modelo tiene un campo 'company' o 'branch__company'
            # Para modelos directos (Product, Supplier):
            if hasattr(self.serializer_class.Meta.model, 'company'):
                return qs.filter(company=user.company)
            # Para modelos indirectos (Inventory, Sale):
            if hasattr(self.serializer_class.Meta.model, 'branch'):
                return qs.filter(branch__company=user.company)
            
        # 4. Si no cumple nada, lista vacía por seguridad
        return qs.none()