from django.db import models
from Apps.Catalogos.Product_Category.models import product_Category
from Apps.Catalogos.Supplier.models import supplier

class product(models.Model):
    idProduct = models.AutoField(primary_key=True)
    nameProduct = models.CharField(max_length=200, verbose_name="Nombre del producto")
    description = models.TextField(blank=True, null=True, verbose_name="Descripcion del producto")
    price_cost = models.DecimalField(decimal_places=2, max_digits=10, default=0.00, verbose_name="Precio Costo del producto")
    price_selling = models.DecimalField(decimal_places=2, max_digits=10, default=0.00, verbose_name="Precio Venta del producto")
    current_stock = models.PositiveIntegerField(default=0, verbose_name="Stock Actual")
    min_stock = models.PositiveIntegerField(default=10, verbose_name="Stock Minimo")
    categoryfk = models.ForeignKey(product_Category, related_name='productos_categoria' ,on_delete=models.PROTECT, verbose_name="Categoría del Producto")
    supplierfk = models.ForeignKey(supplier, related_name='productos_proveedor',on_delete=models.PROTECT, verbose_name="Proveedor del Producto")

    class Meta:
        verbose_name = "Producto"
        verbose_name_plural = "Productos"

    def __str__(self):
        return f"Producto: {self.nameProduct} (Stock: {self.current_stock})"
