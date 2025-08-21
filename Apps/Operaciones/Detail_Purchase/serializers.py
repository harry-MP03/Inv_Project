from rest_framework import serializers
from .models import detail_purchase
from Apps.Operaciones.Product.serializers import  productReadDetail_Serializer
from Apps.Operaciones.Product.models import product

class detailPurchaseSerializer(serializers.ModelSerializer):
    product = productReadDetail_Serializer(read_only=True)

    class Meta:
        model = detail_purchase
        fields = ['idDetailPurchase', 'product', 'quantity', 'unit_cost']


class DetailsPurchaseInput_Serializer(serializers.Serializer):
    productID = serializers.IntegerField()
    quantity = serializers.IntegerField()
    unit_cost = serializers.DecimalField(decimal_places=2, max_digits=10)

    def validate_productID(self, value):
        if not product.objects.filter(pk=value).exists():
            raise serializers.ValidationError(f'El Producto con este ID {value} no existe')
        return value
