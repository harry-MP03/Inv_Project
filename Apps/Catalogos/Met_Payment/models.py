from django.db import models

class metPayment(models.Model):
    idPayment = models.AutoField(primary_key=True)
    namePayment = models.CharField(max_length=100, unique=True, verbose_name="Nombre de forma de pago")
    DescriptionPayment = models.TextField(blank=True, null=True, verbose_name="Descripción de la forma de pago")

    class Meta:
        verbose_name = 'Forma de pago'
        verbose_name_plural = 'Formas de pago'

    def __str__(self):
        return self.namePayment
