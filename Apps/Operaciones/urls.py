from django.urls import path, include

urlpatterns = [
    path('Product/', include('Apps.Operaciones.Product.urls')),
    path('Purchase_product/', include('Apps.Operaciones.Purchase_product.urls')),
    path('Sales_product/', include('Apps.Operaciones.Sales_product.urls')),

]
