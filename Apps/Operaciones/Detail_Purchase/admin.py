from django.contrib import admin

from .models import detail_purchase

@admin.register(detail_purchase)
class detail_purchaseAdmin(admin.ModelAdmin):
    list_display = ['idDetailPurchase','purchaseFK', 'productfk', 'quantity', 'unit_cost']
    search_fields = ['idDetailPurchase']
