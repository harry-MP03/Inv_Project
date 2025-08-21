from django.urls import path
from .views import SalesListApiView

urlpatterns = [
    path("", SalesListApiView.as_view()),
]
