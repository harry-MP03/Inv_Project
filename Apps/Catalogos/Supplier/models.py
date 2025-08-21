from django.db import models

class supplier(models.Model):
    idSupplier = models.AutoField(primary_key=True)
    nameSupplier = models.CharField(max_length=150, verbose_name="Nombre del proveedor")
    contact = models.CharField(max_length=100, blank=True, null=True,verbose_name="Contacto de la persona")
    PhoneNumber = models.CharField(max_length=20, blank=True, null=True ,verbose_name="Numero de telefono")
    email = models.CharField(max_length=100, blank=True, null=True ,verbose_name="Email de la persona")

    class Meta:
        verbose_name = "Proveedor"
        verbose_name_plural = "Proveedores"

    def __str__(self):
        return self.nameSupplier