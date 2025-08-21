from django.contrib import admin

from .models import purchase_product
@admin.register(purchase_product)
class PurchaseProductAdmin(admin.ModelAdmin):
    list_display = ['idPurchase','supplierfk','datePurchase','total_purchase']
    search_fields = ['idPurchase']
