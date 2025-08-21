from rest_framework.serializers import ModelSerializer
from .models import metPayment

class metPaymentSerializer(ModelSerializer):
    class Meta:
        model = metPayment
        fields = '__all__'

class metPaymentNameSerializer(ModelSerializer):
    class Meta:
        model = metPayment
        fields = ['namePayment']