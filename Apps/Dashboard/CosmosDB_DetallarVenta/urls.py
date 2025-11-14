
from django.urls import path
from .views import ReporteDetallarVentaApiView
urlpatterns = [

    path("Detalle/<int:id_venta>/", ReporteDetallarVentaApiView.as_view()),

]
