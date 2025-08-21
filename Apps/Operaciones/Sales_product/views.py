from rest_framework.permissions import IsAuthenticated
from django.db import transaction
from rest_framework import serializers
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema

from Apps.Operaciones.Sales_product.models import sales_product
from Apps.Operaciones.Detail_Sales.models import detailSalesProduct
from Apps.Operaciones.Product.models import product
from Apps.Operaciones.Sales_product.serializers import SalesProductSerializer, SalesProductRegisterSerializer
from config.utils.Pagination import PaginationMixin
import logging.handlers

# Configuracion de el logger
logger = logging.getLogger(__name__)

class SalesListApiView(APIView, PaginationMixin):
    model = sales_product
    #permission_classes = [IsAuthenticated]

    @swagger_auto_schema(responses={200: SalesProductSerializer(many=True)})
    def get(self, request, format=None):
        """Obtener listado de las ventas"""
        logger.info('GET request to list all Sales')
        queryset = sales_product.objects.all().order_by('-dateSales')

        page = self.paginate_queryset(queryset, request)
        if page is not None:
            serializer = SalesProductSerializer(page, many=True)
            logger.info('Paginated response for Sales')
            return self.get_paginated_response(serializer.data)

        serializer = SalesProductSerializer(queryset, many=True)
        logger.info('Returning all Sales without pagination')
        return Response(serializer.data)

    @swagger_auto_schema(request_body=SalesProductRegisterSerializer,responses={201: SalesProductSerializer(many=True)})
    def post(self, request, format=None):
        """Crear un registro de compras"""
        logger.info('POST request to create a new Sale')
        serializer = SalesProductRegisterSerializer(data=request.data)
        if not serializer.is_valid():
            logger.error('Failed to create Purchase: %s', serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        validated_data = serializer.validated_data
        details_data = validated_data.get('details')
        try:
            with transaction.atomic():
             #Preparando los datos base para crear nuestra venta de producto
                data_create = {
                'met_paymentFk_id': validated_data.get('metPayment_id'),
                'customerFk_id': validated_data.get('customer_id')
                }
                #Si en el frontend ha enviado una fecha, se le añade
                if 'dateSales' in validated_data:
                    data_create['dateSales'] = validated_data['dateSales']

                #Se creará el objeto principal de la venta
                new_sale = sales_product.objects.create(**data_create)

                total_sale_calculated = 0

                #Iterando sobre los detalles para crear registros y actualizar el stock
                for details_item in details_data:
                    productID = details_item['productID']
                    quantity_sold = details_item['quantity']

                product_object = product.objects.select_for_update().get(idProduct=productID)

                #Logica del negocio para Validar y disminuir el stock
                if product_object.current_stock < quantity_sold:
                    raise serializers.ValidationError(f"Stock insuficiente para '{product_object.nameProduct}'. Disponible: {product_object.current_stock}")

                product_object.current_stock -= quantity_sold
                product_object.save()

                #Crear el registro del detalle de ventas
                detailSalesProduct.objects.create(
                    saleFk = new_sale,
                    productFK = product_object,
                    quantity_detailSales = quantity_sold,
                    price_Unit = product_object.price_selling
                )
                total_sale_calculated += quantity_sold * product_object.price_selling

                #Actualizando el total en la venta principal
                new_sale.total_sales = round(total_sale_calculated, 2)
                new_sale.save()

                # Devolver la venta recien creada y serializada para confirmar el registro
                responseSales_serializer = SalesProductSerializer(new_sale)
                logger.info('Sale created successfully')
                return Response(responseSales_serializer.data, status=status.HTTP_201_CREATED)

        except product.DoesNotExist:
            return Response({"error": "Uno de los productos en la venta no ha sido encontrado"}, status=status.HTTP_404_NOT_FOUND)
        except serializers.ValidationError as e:
            return Response({"error": e.detail}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": f"Ocurrió un error inesperado: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)