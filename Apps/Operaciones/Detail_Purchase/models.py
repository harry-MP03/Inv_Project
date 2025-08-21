from django.db import models
from Apps.Operaciones.Product.models import product
from Apps.Operaciones.Purchase_product.models import purchase_product

class detail_purchase(models.Model):
    idDetailPurchase = models.AutoField(primary_key=True)
    #el related name sirve para crear relaciones inversas para en este caso, mostrar los detalles de la compra en compras para un facil acceso
    purchaseFK = models.ForeignKey(purchase_product, related_name='detalles_compra', on_delete=models.CASCADE, verbose_name='Compra')
    productfk = models.ForeignKey(product, on_delete=models.PROTECT, verbose_name='Producto')
    quantity = models.PositiveIntegerField(verbose_name='Cantidad comprada')
    unit_cost = models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Costo unitario en la compra')

    class Meta:
        verbose_name = "Detalle de Compra"
        verbose_name_plural = "Detalles de compras"

    def __str__(self):
        return f"{self.quantity} x {self.productfk.nameProduct} en compra #{self.purchaseFK.idPurchase}"
