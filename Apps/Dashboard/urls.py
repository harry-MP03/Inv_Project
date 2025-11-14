
from django.urls import path, include

urlpatterns = [
    path('CategoriaVentaTotal-2025/', include('Apps.Dashboard.CategoriaVentaTotal_2025.urls')),
    path('TopClientes-General/', include('Apps.Dashboard.TopClientes.urls')),
    path('VentasMensual-2025/', include('Apps.Dashboard.VentasMensualesGeneral.urls')),
    path('CosmosDB-ListarProductos/', include('Apps.Dashboard.CosmosDB_ListarProductos.urls')),
    path('CosmosDB-DetalleVenta/', include('Apps.Dashboard.CosmosDB_DetallarVenta.urls'))
]
