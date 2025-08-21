from django.db import models

class product_Category(models.Model):
    idCategory = models.AutoField(primary_key=True)
    nameCategory = models.CharField(max_length=160, unique=True, verbose_name="Categorías")

    class Meta:
        verbose_name = 'Categoría de Producto'
        verbose_name_plural = 'Categorías de Producto'

    def __str__(self):
        return self.nameCategory