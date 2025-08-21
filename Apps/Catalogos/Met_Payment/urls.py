
from django.urls import path
from .views import metPaymentApiview, metPayment_PPD_Apiview
urlpatterns = [

    path("", metPaymentApiview.as_view()),
    path('<int:pk>', metPayment_PPD_Apiview.as_view()),

]
