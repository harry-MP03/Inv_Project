from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from .models import purchase_product
from Apps.Operaciones.Detail_Purchase.serializers import  detailPurchaseSerializer, DetailsPurchaseInput_Serializer
from Apps.Catalogos.Supplier.serializers import supplierNameSerializer
from Apps.Catalogos.Supplier.models import supplier

class PurchaseSerializer(ModelSerializer):
    supplierName = supplierNameSerializer(read_only=True,source='supplierfk')
    detalles_compra = detailPurchaseSerializer(read_only=True, many=True)

    class Meta:
        model = purchase_product
        fields = ['idPurchase', 'supplierName', 'datePurchase', 'total_purchase', 'detalles_compra']

class PurchaseRegisterSerializer(serializers.Serializer):
    supplier_id = serializers.IntegerField()
    details = DetailsPurchaseInput_Serializer(many=True)
    datePurchase = serializers.DateTimeField(required=False)

    def validate_supplier_id(self, value):
        if not supplier.objects.filter(pk=value).exists():
            raise serializers.ValidationError(f"El proveedor con este ID {value} no existe")
        return value

