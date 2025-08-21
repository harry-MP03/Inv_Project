
from django.urls import path
from .views import CategoryListCreateAPIView, CategoryDetailAPIView
urlpatterns = [

    path("", CategoryListCreateAPIView.as_view()),
    path('<int:pk>', CategoryDetailAPIView.as_view()),

]
