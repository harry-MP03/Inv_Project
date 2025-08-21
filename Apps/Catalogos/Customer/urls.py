
from django.urls import path
from .views import CustomerListCreateAPIView,CustomerDetailAPIView
urlpatterns = [

    path("", CustomerListCreateAPIView.as_view()),
    path('<int:pk>', CustomerDetailAPIView.as_view()),

]
