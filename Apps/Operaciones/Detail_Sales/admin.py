from django.contrib import admin

from .models import detailSalesProduct

@admin.register(detailSalesProduct)
class detailSalesProductAdmin(admin.ModelAdmin):
    list_display = ['idDetailSalesProduct','saleFk','productFK','quantity_detailSales','price_Unit']
    search_fields = ['idDetailSalesProduct']
