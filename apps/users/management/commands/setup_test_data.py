import random
from itertools import cycle
from django.core.management.base import BaseCommand
from django.utils import timezone
from apps.users.models import User, Company, Subscription
from apps.products.models import Branch, Product, Inventory, Supplier

class Command(BaseCommand):
    help = 'Puebla la base de datos con datos masivos y realistas (2 Empresas, 20+ Productos)'

    def generar_rut(self):
        """Genera RUTs válidos al azar."""
        cuerpo = random.randint(5000000, 25000000)
        cuerpo_str = str(cuerpo)
        revertido = map(int, reversed(cuerpo_str))
        factors = cycle(range(2, 8))
        s = sum(d * f for d, f in zip(revertido, factors))
        res = (-s) % 11
        dv = 'K' if res == 10 else str(res)
        return f"{cuerpo}-{dv}"

    def handle(self, *args, **kwargs):
        self.stdout.write("🏭 Iniciando generación de datos masiva...")

        # --- EMPRESA 1: FARMACIA ---
        company_farma, _ = Company.objects.get_or_create(
            name="Farmacia Bienestar",
            defaults={'rut': "76111222-8", 'address': "Av. Alemania 0123, Temuco"}
        )
        Subscription.objects.get_or_create(
            company=company_farma,
            defaults={'plan_name': 'PREMIUM', 'start_date': timezone.now().date(), 'end_date': timezone.now().date() + timezone.timedelta(days=365)}
        )

        # Sucursal Farmacia
        branch_farma, _ = Branch.objects.get_or_create(
            company=company_farma, name="Casa Matriz", defaults={'address': "Centro", 'phone': "452999999"}
        )

        # --- EMPRESA 2: MINIMARKET (Para probar multi-tenant) ---
        company_market, _ = Company.objects.get_or_create(
            name="Minimarket El Vecino",
            defaults={'rut': "12345678-5", 'address': "Villa Los Rios 456, Padre Las Casas"}
        )
        Subscription.objects.get_or_create(
            company=company_market,
            defaults={'plan_name': 'STANDARD', 'start_date': timezone.now().date(), 'end_date': timezone.now().date() + timezone.timedelta(days=365)}
        )
        branch_market, _ = Branch.objects.get_or_create(
            company=company_market, name="Local Único", defaults={'address': "Calle Principal", 'phone': "987654321"}
        )

        # --- USUARIOS ---
        users_config = [
            # (User, Role, Company, Pass)
            ('superadmin', 'SUPER_ADMIN', None, 'admin123'),
            ('admin_farma', 'ADMIN_CLIENTE', company_farma, 'admin123'),
            ('gerente_farma', 'GERENTE', company_farma, 'admin123'),
            ('cajero_farma', 'VENDEDOR', company_farma, 'admin123'),
            ('dueno_market', 'ADMIN_CLIENTE', company_market, 'admin123'),
            ('cajero_market', 'VENDEDOR', company_market, 'admin123'),
        ]

        for uname, role, comp, pwd in users_config:
            if not User.objects.filter(username=uname).exists():
                User.objects.create_user(
                    username=uname, email=f"{uname}@temucosoft.cl", password=pwd,
                    role=role, company=comp, rut=self.generar_rut()
                )
                self.stdout.write(f"👤 Usuario creado: {uname}")

        # --- PROVEEDORES REALISTAS (5 para Farmacia) ---
        proveedores_farma = [
            ("Laboratorio Chile", "ventas@labchile.cl"),
            ("Laboratorio Saval", "contacto@saval.cl"),
            ("Droguería Ñuñoa", "pedidos@droguerianunoa.cl"),
            ("Insumos Médicos Sur", "ventas@insumosur.cl"),
            ("Distribuidora Farmacéutica", "contacto@distrifarma.cl"),
        ]
        
        for name, email in proveedores_farma:
            Supplier.objects.get_or_create(
                company=company_farma, name=name,
                defaults={'rut': self.generar_rut(), 'contact_email': email, 'phone': "222222222"}
            )

        # --- PROVEEDORES REALISTAS (3 para Market) ---
        proveedores_market = [
            ("Coca Cola Embonor", "preventa@embonor.cl"),
            ("CCU", "pedidos@ccu.cl"),
            ("Soprole", "ventas@soprole.cl"),
        ]
        
        for name, email in proveedores_market:
            Supplier.objects.get_or_create(
                company=company_market, name=name,
                defaults={'rut': self.generar_rut(), 'contact_email': email, 'phone': "600600600"}
            )

        self.stdout.write(self.style.SUCCESS("✅ Proveedores cargados."))

        # --- PRODUCTOS FARMACIA (15 Items) ---
        farma_products = [
            ('PAR001', 'Paracetamol 500mg (Caja 16)', 1590, 450, 'Medicamentos'),
            ('IBU002', 'Ibuprofeno 400mg (Caja 20)', 2990, 800, 'Medicamentos'),
            ('AMO003', 'Amoxicilina 500mg', 3500, 1200, 'Antibióticos'),
            ('LOR004', 'Loratadina 10mg', 1200, 300, 'Antialérgicos'),
            ('VIT005', 'Vitamina C 1000mg', 4990, 2500, 'Vitaminas'),
            ('ENS006', 'Ensure Polvo Vainilla', 18990, 14000, 'Nutrición'),
            ('PAN007', 'Pañales Adulto M', 12990, 8000, 'Insumos'),
            ('ALC008', 'Alcohol Gel 1L', 2500, 1000, 'Aseo'),
            ('MAS009', 'Mascarillas x50', 3000, 1500, 'Insumos'),
            ('CRE010', 'Crema Hidratante Piel', 5990, 3000, 'Dermocosmética'),
            ('JAR011', 'Jarabe para la Tos', 4500, 2000, 'Respiratorio'),
            ('ASP012', 'Aspirina 100mg', 1800, 600, 'Medicamentos'),
            ('OME013', 'Omeprazol 20mg', 2200, 700, 'Gástrico'),
            ('BLO014', 'Bloqueador Solar FPS50', 8990, 4500, 'Dermocosmética'),
            ('CEPI015', 'Cepillo Dental Suave', 1500, 500, 'Higiene'),
        ]

        for sku, name, price, cost, cat in farma_products:
            p, _ = Product.objects.get_or_create(
                company=company_farma, sku=sku,
                defaults={'name': name, 'description': name, 'price': price, 'cost': cost, 'category': cat}
            )
            # Stock aleatorio entre 20 y 100
            Inventory.objects.update_or_create(
                branch=branch_farma, product=p,
                defaults={'stock': random.randint(20, 100), 'reorder_point': 10}
            )

        # --- PRODUCTOS MARKET (5 Items) ---
        market_products = [
            ('COCA3L', 'Coca Cola 3 Litros', 3200, 1800, 'Bebidas'),
            ('PANMT', 'Pan Marraqueta KG', 1990, 1000, 'Panadería'),
            ('LECHE1', 'Leche Entera 1L', 1100, 700, 'Lácteos'),
            ('ARR1KG', 'Arroz Grado 2', 1300, 800, 'Abarrotes'),
            ('ACE1L', 'Aceite Vegetal', 2100, 1200, 'Abarrotes'),
        ]

        for sku, name, price, cost, cat in market_products:
            p, _ = Product.objects.get_or_create(
                company=company_market, sku=sku,
                defaults={'name': name, 'description': name, 'price': price, 'cost': cost, 'category': cat}
            )
            Inventory.objects.update_or_create(
                branch=branch_market, product=p,
                defaults={'stock': random.randint(10, 50), 'reorder_point': 5}
            )

        self.stdout.write(self.style.SUCCESS("✨ ¡Base de datos poblada con éxito!"))
        self.stdout.write("------------------------------------------------")
        self.stdout.write("Credenciales Generadas (Pass: admin123):")
        self.stdout.write("1. admin_farma (Ve datos de Farmacia)")
        self.stdout.write("2. dueno_market (Ve datos de Market)")
        self.stdout.write("3. superadmin (Gestión Global)")