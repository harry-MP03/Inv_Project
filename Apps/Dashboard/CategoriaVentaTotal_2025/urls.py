
from django.urls import path
from .views import ReporteVentasCategoriaApiView
urlpatterns = [

    path("Ventas-Categoria", ReporteVentasCategoriaApiView.as_view()),

]
