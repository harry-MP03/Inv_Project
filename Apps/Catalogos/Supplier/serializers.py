from rest_framework.serializers import ModelSerializer
from .models import supplier

class supplierSerializer(ModelSerializer):
    class Meta:
        model = supplier
        fields = '__all__'

class supplierNameSerializer(ModelSerializer):
    class Meta:
        model = supplier
        fields = ['nameSupplier']