
from django.urls import path, include

urlpatterns = [
    path('Met_Payment/', include('Apps.Catalogos.Met_Payment.urls')),
    path('Customer/', include('Apps.Catalogos.Customer.urls')),
    path('Product_Category/', include('Apps.Catalogos.Product_Category.urls')),
    path('Supplier/', include('Apps.Catalogos.Supplier.urls')),
]
