
from django.urls import path
from .views import ReporteTopClientesApiview
urlpatterns = [

    path("Top-5-ClientesGastoTotal", ReporteTopClientesApiview.as_view()),

]
