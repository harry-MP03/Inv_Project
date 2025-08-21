from rest_framework.serializers import ModelSerializer
from .models import customer

class CustomerSerializer(ModelSerializer):
    class Meta:
        model = customer
        fields = '__all__'

class CustomerNameSerializer(ModelSerializer):
    class Meta:
        model = customer
        fields = ['CustName']