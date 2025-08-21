from django.db import models

class customer(models.Model):
    idCustomer = models.AutoField(primary_key=True)
    CustName = models.CharField(max_length=120, verbose_name='Nombre del Cliente')
    CustLastName = models.CharField(max_length=120, blank=True,null=True,verbose_name='Apellido del Cliente')
    Cust_phone = models.CharField(max_length=20, blank=True,null=True,verbose_name='Telefono del cliente')
    Cust_email = models.CharField(max_length=120, blank=True,null=True,verbose_name='Email del cliente')
    CustAddress = models.CharField(max_length=120, blank=True,null=True,verbose_name='Direccion del cliente')

    class Meta:
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'
    def __str__(self):
        return f"{self.CustName} {self.CustLastName}" \
            if self.CustLastName else self.CustName
