from django.db import models
from Apps.Catalogos.Customer.models import customer
from Apps.Catalogos.Met_Payment.models import metPayment
from django.conf import settings
from django.utils import timezone

class sales_product(models.Model):
    idSalesProduct = models.AutoField(primary_key=True)
    dateSales = models.DateTimeField(default=timezone.now, verbose_name="Fecha de Venta")
    total_sales = models.DecimalField(max_digits=10, decimal_places=2, default=0.00 ,verbose_name="Total de venta")
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        verbose_name="Vendedor",
        null=True)
    met_paymentFk = models.ForeignKey(metPayment, on_delete=models.PROTECT, verbose_name="Forma de pago")
    customerFk = models.ForeignKey(customer, on_delete=models.SET_NULL, null=True, verbose_name="Cliente")

    class Meta:
        verbose_name = "Detalle de venta"
        verbose_name_plural = "Detalles de ventas"

    def __str__(self):
        return f"{self.met_paymentFk.namePayment} {self.customerFk.CustName}"
