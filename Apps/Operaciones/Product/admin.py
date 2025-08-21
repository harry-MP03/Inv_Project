from django.contrib import admin

from .models import product
@admin.register(product)
class product_Admin(admin.ModelAdmin):
    list_display = ['idProduct','nameProduct', 'description', 'price_cost', 'price_selling', 'current_stock',
                    'min_stock','categoryfk', 'supplierfk']
    search_fields = ['nameProduct']