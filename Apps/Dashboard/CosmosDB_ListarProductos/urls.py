
from django.urls import path
from .views import ReporteListaPrductosApiView
urlpatterns = [

    path("Lista-Productos", ReporteListaPrductosApiView.as_view()),

]
