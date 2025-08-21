from django.contrib import admin
from .models import product_Category

@admin.register(product_Category)
class product_CategoryAdmin(admin.ModelAdmin):
    list_display =['idCategory','nameCategory']
    search_fields = ['nameCategory']