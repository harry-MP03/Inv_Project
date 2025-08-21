from django.contrib import admin

from Apps.Catalogos.Customer.models import customer

@admin.register(customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['idCustomer','CustName','CustLastName', 'Cust_phone', 'Cust_email', 'CustAddress']
    search_fields = ['CustName','Cust_email','Cust_phone']