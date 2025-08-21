from django.db import models
from django.utils import timezone

from Apps.Catalogos.Supplier.models import supplier

class purchase_product(models.Model):
    idPurchase = models.AutoField(primary_key=True)
    supplierfk = models.ForeignKey(supplier, on_delete=models.PROTECT, verbose_name="Proveedor")
    datePurchase = models.DateTimeField(default=timezone.now ,verbose_name="Fecha de Compra")
    total_purchase = models.DecimalField(max_digits=10, decimal_places=2, default=0.00 ,verbose_name="Total de la compra")

    class Meta:
        verbose_name = "Compra de producto"
        verbose_name_plural = "Compras de productos"

    def __str__(self):
        return f"Compra #{self.idPurchase} a {self.supplierfk.nameSupplier} - {self.datePurchase.strftime('%d/%m/%Y')}"


