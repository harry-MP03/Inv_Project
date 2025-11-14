
from django.urls import path
from .views import VentasMensualesGeneralApiView
urlpatterns = [

    path("Cronología-VentasPorMes-2025", VentasMensualesGeneralApiView.as_view()),

]
