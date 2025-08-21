from rest_framework.serializers import ModelSerializer,CharField
from .models import product_Category

class ProductCategorySerializer(ModelSerializer):
    class Meta:
        model = product_Category
        fields = '__all__'

class ProductCategoryNameSerializer(ModelSerializer):
    class Meta:
        model = product_Category
        fields = ['nameCategory']