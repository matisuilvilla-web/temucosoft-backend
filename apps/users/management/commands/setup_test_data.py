import random
from django.core.management.base import BaseCommand
from django.utils import timezone
from apps.users.models import User, Company, Subscription
from apps.products.models import Branch, Product, Inventory, Supplier

class Command(BaseCommand):
    help = 'Genera datos de prueba para TemucoSoft (Usuarios, Roles, Productos, Stock)'

    def handle(self, *args, **kwargs):
        self.stdout.write("Iniciando generación de datos de prueba...")

        # 1. Crear Empresa (Tenant) - Ejemplo: Farmacia
        company, created = Company.objects.get_or_create(
            name="Farmacia La Salud",
            defaults={'rut': "76111222-3", 'address': "Av. Alemania 123"}
        )
        if created:
            self.stdout.write(f"Empresa creada: {company.name}")
        
        # 2. Crear Suscripción Premium
        Subscription.objects.get_or_create(
            company=company,
            defaults={
                'plan_name': 'PREMIUM',
                'start_date': timezone.now().date(),
                'end_date': timezone.now().date() + timezone.timedelta(days=365),
                'is_active': True
            }
        )

        # 3. Crear Usuarios por Rol
        # Formato: (Username, Email, Role, Password)
        users_data = [
            ('superadmin', 'super@temucosoft.cl', 'SUPER_ADMIN', 'admin123'),
            ('admin_cliente', 'dueno@lasalud.cl', 'ADMIN_CLIENTE', 'admin123'),
            ('gerente', 'gerente@lasalud.cl', 'GERENTE', 'admin123'),
            ('vendedor', 'caja1@lasalud.cl', 'VENDEDOR', 'admin123'),
        ]

        for username, email, role, pwd in users_data:
            if not User.objects.filter(username=username).exists():
                # El superadmin lo dejamos sin compañía para que sea global, el resto a la Farmacia
                user_company = None if role == 'SUPER_ADMIN' else company
                
                User.objects.create_user(
                    username=username,
                    email=email,
                    password=pwd,
                    role=role,
                    company=user_company,
                    rut=f"11222333-{random.randint(1,9)}"
                )
                self.stdout.write(self.style.SUCCESS(f"Usuario creado: {username} (Rol: {role}) / Pass: {pwd}"))
            else:
                self.stdout.write(self.style.WARNING(f"Usuario {username} ya existía."))

        # 4. Crear Sucursal y Proveedor
        branch, _ = Branch.objects.get_or_create(
            company=company,
            name="Sucursal Centro",
            defaults={'address': "Calle Bulnes 555", 'phone': "452123456"}
        )
        
        supplier, _ = Supplier.objects.get_or_create(
            company=company,
            name="Laboratorio Chile",
            defaults={'rut': "99555444-2", 'contact_email': "ventas@labchile.cl", 'phone': "22222222"}
        )

        # 5. Crear Productos e Inventario
        products_list = [
            ('PARACETAMOL', 'Paracetamol 500mg', 1500, 500, 'Medicamentos'),
            ('IBUPROFENO', 'Ibuprofeno 400mg', 2500, 800, 'Medicamentos'),
            ('JABON', 'Jabón Líquido', 3000, 1200, 'Aseo'),
            ('PAÑALES', 'Pañales XG', 12000, 8000, 'Infantil'),
            ('BEBIDA', 'Bebida 3L', 2800, 1500, 'Bebestibles'),
        ]

        for sku, name, price, cost, cat in products_list:
            prod, created = Product.objects.get_or_create(
                company=company,
                sku=sku,
                defaults={
                    'name': name, 'description': name, 
                    'price': price, 'cost': cost, 'category': cat
                }
            )
            
            # Inicializar inventario si el producto se creó o si no tiene stock
            Inventory.objects.get_or_create(
                branch=branch,
                product=prod,
                defaults={'stock': 100, 'reorder_point': 10}
            )
        
        self.stdout.write(self.style.SUCCESS("¡Datos de prueba generados exitosamente!"))