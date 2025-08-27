import random
from datetime import timedelta
from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils import timezone
from faker import Faker

# Importamdp todos los modelos que se necesita poblar

#Catalogos
from Apps.Seguridad.Usuarios.models import User
from Apps.Catalogos.Product_Category.models import product_Category
from Apps.Catalogos.Supplier.models import supplier
from Apps.Operaciones.Product.models import product
from Apps.Catalogos.Met_Payment.models import metPayment
from Apps.Catalogos.Customer.models import customer

#Flujo de compras
from Apps.Operaciones.Purchase_product.models import purchase_product
from Apps.Operaciones.Detail_Purchase.models import detail_purchase

#Flujo de Ventas
from Apps.Operaciones.Sales_product.models import sales_product
from Apps.Operaciones.Detail_Sales.models import detailSalesProduct

class Command(BaseCommand):
    help = 'Crear datos de prueba realistas para toda la base de datos'

    @transaction.atomic
    def handle(self, *args, **options):
        self.stdout.write('Eliminando datos antiguos...')
        #Se eliminan en orden inverso para evitar errores de llaves foráneas
        detailSalesProduct.objects.all().delete()
        sales_product.objects.all().delete()
        detail_purchase.objects.all().delete()
        purchase_product.objects.all().delete()
        product.objects.all().delete()
        customer.objects.all().delete()
        metPayment.objects.all().delete()
        product_Category.objects.all().delete()
        supplier.objects.all().delete()
        User.objects.filter(is_superuser=False).delete()

        self.stdout.write('Creando nuevos datos de prueba...')
        fake = Faker('es_ES')

        # --- Crear Catálogos ---
        usuarios = [User.objects.create_user(f'cajero{i}', 'password123', first_name=fake.first_name(),
                                             last_name=fake.last_name()) for i in range(30)]
        self.stdout.write(f"✓ {len(usuarios)} usuarios creados.")

        categorias = [product_Category.objects.create(nameCategory=nombre) for nombre in
                      ['Bebidas', 'Snacks', 'Lacteos', 'Abarrotes', 'Limpieza']]
        self.stdout.write(f"✓ {len(categorias)} categorías creadas.")

        proveedores = [
            supplier.objects.create(nameSupplier=fake.company(), contact=fake.name(), PhoneNumber=fake.phone_number(),
                                    email=fake.email()) for _ in range(15)]
        self.stdout.write(f"✓ {len(proveedores)} proveedores creados.")

        clientes = [
            customer.objects.create(CustName=fake.name(), CustLastName=fake.last_name(), Cust_phone=fake.phone_number(),
                                    Cust_email=fake.email()) for _ in range(2350)]
        self.stdout.write(f"✓ {len(clientes)} clientes creados.")

        metodos_pago = [metPayment.objects.create(namePayment=nombre) for nombre in
                        ['Efectivo', 'Tarjeta de crédito', 'Transferencia']]
        self.stdout.write(f"✓ {len(metodos_pago)} métodos de pago creados.")

        # --- Crear Productos ---
        productos = []
        for _ in range(100):
            precio_costo = round(random.uniform(5.0, 150.0), 2)
            prod = product.objects.create(
                nameProduct=fake.bs().capitalize(),
                price_cost=precio_costo,
                price_selling=round(precio_costo * random.uniform(1.25, 1.6), 2),
                current_stock=random.randint(50, 200),
                min_stock=15,
                categoryfk=random.choice(categorias),
                supplierfk=random.choice(proveedores)
            )
            productos.append(prod)
        self.stdout.write(f"✓ {len(productos)} productos creados.")

        #Crear Compras y sus Detalles
        for _ in range(2350):
            compra = purchase_product.objects.create(supplierfk=random.choice(proveedores))
            total_compra = 0
            for _ in range(random.randint(1, 8)):
                producto_comprado = random.choice(productos)
                cantidad = random.randint(5, 50)
                costo = producto_comprado.price_cost
                detail_purchase.objects.create(
                    purchaseFK=compra, productfk=producto_comprado, quantity=cantidad, unit_cost=costo
                )
                producto_comprado.current_stock += cantidad
                producto_comprado.save()

                total_compra += cantidad * costo
            compra.total_purchase = round(total_compra, 2)
            compra.save()
        self.stdout.write("✓ 2350 compras con detalles creadas.")

        #Crear Ventas y sus Detalles
        for _ in range(2350):
            fecha_aleatoria = timezone.now() - timedelta(days=random.randint(0, 365), hours=random.randint(0, 23))
            venta = sales_product.objects.create(
                user=random.choice(usuarios),
                customerFk=random.choice(clientes),
                met_paymentFk=random.choice(metodos_pago),
                dateSales=fecha_aleatoria
            )
            total_venta = 0
            for _ in range(random.randint(1, 5)):
                producto_vendido = random.choice(productos)
                cantidad = random.randint(1, 10)
                if producto_vendido.current_stock >= cantidad:
                    precio = producto_vendido.price_selling
                    detailSalesProduct.objects.create(
                        saleFk=venta, productFK=producto_vendido, quantity_detailSales=cantidad, price_Unit=precio
                    )
                    producto_vendido.current_stock -= cantidad
                    producto_vendido.save()
                    total_venta += cantidad * precio
            venta.total_sales = round(total_venta, 2)
            venta.save()
        self.stdout.write("✓ 2350 ventas con detalles y actualización de stock creadas.")

        self.stdout.write(self.style.SUCCESS('¡Poblado de datos completado exitosamente!'))