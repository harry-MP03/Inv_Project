from django.urls import path
from .views import PurchaseListApiview
urlpatterns = [
    path("", PurchaseListApiview.as_view()),

]
