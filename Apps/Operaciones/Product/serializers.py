from rest_framework.serializers import ModelSerializer
from .models import product
from Apps.Catalogos.Supplier.serializers import supplierNameSerializer
from Apps.Catalogos.Product_Category.serializers import ProductCategoryNameSerializer


class productReadDetail_Serializer(ModelSerializer):
    category = ProductCategoryNameSerializer(read_only=True, source='categoryfk')
    supplier = supplierNameSerializer(read_only=True, source='supplierfk')
    class Meta:
        model = product
        fields = ['idProduct','nameProduct','description','price_cost','price_selling',
                 'current_stock','min_stock','category','supplier']

class productSerializer(ModelSerializer):
    class Meta:
        model = product
        fields = '__all__'