from django.db import models  # Importa la clase base para definir modelos de base de datos en Django
from apps.users.models import Company  # Importa el modelo Company desde la aplicación 'users' para establecer relaciones
from utils.validators import validar_rut, validar_positivo  # Importa validadores personalizados para validar RUT y valores positivos

# Modelo que representa un proveedor (Supplier)
class Supplier(models.Model):
    # Relación de clave foránea con el modelo 'Company'. 
    # El proveedor está asociado a una empresa específica. Si la empresa se elimina, también se elimina el proveedor.
    company = models.ForeignKey(Company, on_delete=models.CASCADE)  # Multi-tenancy
    name = models.CharField(max_length=100)  # Nombre del proveedor, máximo 100 caracteres
    rut = models.CharField(max_length=20, validators=[validar_rut])  # RUT del proveedor, validado con el validador 'validar_rut'
    contact_email = models.EmailField()  # Correo electrónico de contacto del proveedor
    phone = models.CharField(max_length=20)  # Número de teléfono del proveedor

    # Método que devuelve el nombre del proveedor como representación en cadena
    def __str__(self):
        return self.name

# Modelo que representa una sucursal de una empresa (Branch)
class Branch(models.Model):
    # Relación de clave foránea con el modelo 'Company'. 
    # Cada sucursal pertenece a una empresa específica.
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)  # Nombre de la sucursal
    address = models.CharField(max_length=200)  # Dirección de la sucursal
    phone = models.CharField(max_length=20)  # Teléfono de la sucursal

    # Método que devuelve el nombre de la sucursal y el nombre de la empresa asociada como representación en cadena
    def __str__(self):
        return f"{self.name} - {self.company.name}"

# Modelo que representa un producto (Product)
class Product(models.Model):
    # Relación de clave foránea con el modelo 'Company'. 
    # Cada producto pertenece a una empresa.
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    sku = models.CharField(max_length=50)  # SKU (Stock Keeping Unit) del producto, identificador único
    name = models.CharField(max_length=150)  # Nombre del producto
    description = models.TextField(blank=True)  # Descripción del producto (opcional)
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[validar_positivo])  # Precio del producto, validado con 'validar_positivo'
    cost = models.DecimalField(max_digits=10, decimal_places=2, validators=[validar_positivo])  # Costo del producto, validado con 'validar_positivo'
    category = models.CharField(max_length=50)  # Categoría del producto

    # Asegura que cada producto tenga un SKU único por empresa.
    class Meta:
        unique_together = ('company', 'sku')

    # Método que devuelve el nombre del producto como representación en cadena
    def __str__(self):
        return self.name

# Modelo que representa el inventario de una sucursal (Inventory)
class Inventory(models.Model):
    # Relación de clave foránea con el modelo 'Branch'. 
    # Cada registro de inventario está asociado a una sucursal.
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, related_name='inventory')
    # Relación de clave foránea con el modelo 'Product'. 
    # Cada registro de inventario está asociado a un producto específico.
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='stock_records')
    # Cantidad de producto disponible en el inventario de la sucursal
    stock = models.IntegerField(default=0, validators=[validar_positivo])  # Se valida que el stock sea un valor positivo
    # Punto de reorden de inventario, es decir, la cantidad mínima en stock para generar una nueva orden
    reorder_point = models.IntegerField(default=5)

    # Asegura que cada combinación de sucursal y producto sea única en el inventario.
    class Meta:
        unique_together = ('branch', 'product')
    
    # Método que devuelve el nombre del producto junto con el nombre de la sucursal y la cantidad en stock como representación en cadena
    def __str__(self):
        return f"{self.product.name} @ {self.branch.name}: {self.stock}"
