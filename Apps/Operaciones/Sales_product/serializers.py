from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from .models import sales_product
from Apps.Operaciones.Detail_Sales.serializers import  DetailSalesSerializer, Details_SalesInputSerializer
from Apps.Catalogos.Met_Payment.serializers import metPaymentNameSerializer
from Apps.Catalogos.Customer.serializers import CustomerNameSerializer

from Apps.Catalogos.Customer.models import customer
from Apps.Catalogos.Met_Payment.models import metPayment

class SalesProductSerializer(ModelSerializer):
    met_payment = metPaymentNameSerializer(read_only=True, source='met_paymentFk')
    customer = CustomerNameSerializer(read_only=True, source='customerFk')

    detalles_Ventas = DetailSalesSerializer(many=True,read_only=True)

    class Meta:
        model = sales_product
        fields = ['idSalesProduct', 'dateSales', 'total_sales', 'met_payment', 'customer', 'detalles_Ventas']

class SalesProductRegisterSerializer(serializers.Serializer):
    metPayment_id = serializers.IntegerField()
    customer_id = serializers.IntegerField(required=False, allow_null=True)
    details = Details_SalesInputSerializer(many=True)
    dateSales = serializers.DateTimeField(required=False)

    def validate_metPayment_id(self, value):
        if not metPayment.objects.filter(pk=value).exists():
            raise serializers.ValidationError("La forma de pago con este ID no existe en los registros")
        return value
    def validate_customer_id(self, value):
        if not customer.objects.filter(pk=value).exists():
            raise serializers.ValidationError("El cliente con este ID no existe en los registros")
        return value
    def validate_details(self, value):
        if not value:
            raise serializers.ValidationError("La lista de detalles no puede estar vacía")
        return value