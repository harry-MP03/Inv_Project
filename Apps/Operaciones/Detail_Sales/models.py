from django.db import models
from Apps.Operaciones.Sales_product.models import sales_product
from Apps.Operaciones.Product.models import product

class detailSalesProduct(models.Model):
    idDetailSalesProduct = models.AutoField(primary_key=True)
    saleFk = models.ForeignKey(sales_product, related_name='detalles_Ventas',on_delete=models.CASCADE,verbose_name='Detalle de Ventas')
    productFK = models.ForeignKey(product, on_delete=models.PROTECT,verbose_name='Producto')
    quantity_detailSales = models.PositiveIntegerField(verbose_name='Cantidad Vendida')
    price_Unit = models.DecimalField(decimal_places=2,max_digits=10,verbose_name='Precio Unitario en la venta')

    class Meta:
        verbose_name = 'Detalle de ventas'
        verbose_name_plural = 'Detalles de ventas'

    def __str__(self):
        return f"{self.quantity_detailSales} x {self.productFK.nameProduct} en venta #{self.saleFk.idSalesProduct}"