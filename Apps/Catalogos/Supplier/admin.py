from django.contrib import admin

from Apps.Catalogos.Supplier.models import supplier

@admin.register(supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ['idSupplier','nameSupplier','contact','PhoneNumber','email']
    search_fields = ['nameSupplier']
