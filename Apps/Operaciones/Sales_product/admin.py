from django.contrib import admin

from .models import sales_product

@admin.register(sales_product)
class SalesProductAdmin(admin.ModelAdmin):
    list_display = ['idSalesProduct','dateSales','total_sales','met_paymentFk','customerFk']
    search_fields = ['idSalesProduct']
