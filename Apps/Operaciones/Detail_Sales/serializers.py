from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from .models import detailSalesProduct
from Apps.Operaciones.Product.serializers import  productReadDetail_Serializer
from Apps.Operaciones.Product.models import product

class DetailSalesSerializer(ModelSerializer):
    product = productReadDetail_Serializer(read_only=True)

    class Meta:
        model = detailSalesProduct
        fields = ['idDetailSalesProduct','product','quantity_detailSales', 'price_Unit']

#Serializador que detalla los productos provenientes de la petición de ventas
class Details_SalesInputSerializer(serializers.Serializer):
    productID = serializers.IntegerField()
    quantity = serializers.IntegerField()

    def validate_ProductID(self, value):
        #Se verifica de que el producto exista
        if not product.objects.filter(pk=value).exists():
            raise serializers.ValidationError("El producto con este ID no existe en los registros")
        return value
