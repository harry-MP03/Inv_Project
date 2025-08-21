from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics, filters
from django.db import transaction

from config.utils.Pagination import PaginationMixin

from .models import purchase_product
from Apps.Operaciones.Product.models import product
from Apps.Operaciones.Detail_Purchase.models import detail_purchase

from .serializers import PurchaseSerializer, PurchaseRegisterSerializer
from drf_yasg.utils import swagger_auto_schema

from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated

from ...permissions import CustomPermission
from config.utils.Pagination import PaginationMixin
import logging.handlers

# Configuracion de el logger
logger = logging.getLogger(__name__)

class PurchaseListApiview(PaginationMixin,APIView):
    model = purchase_product
    #permission_classes = [IsAuthenticated]

    @swagger_auto_schema(responses={200: PurchaseSerializer(many=True)})
    def get(self, request, format=None):
        """Obtener el listado de las compras"""
        logger.info('GET request to list all Purchases')
        queryset = purchase_product.objects.all().order_by('-datePurchase')
        page = self.paginate_queryset(queryset, request)

        if page is not None:
            serializer = PurchaseSerializer(page, many=True)
            logger.info('Paginated response for Purchases')
            return self.get_paginated_response(serializer.data)

        serializer = PurchaseSerializer(queryset, many=True)
        logger.info('Returning all Purchases without pagination')
        return Response(serializer.data)

    @swagger_auto_schema(request_body=PurchaseRegisterSerializer,responses={201: PurchaseSerializer()})
    def post(self, request, format=None):
        """Crear un registro de compras
        """
        logger.info('POST request to create a new Purchase')
        serializer = PurchaseRegisterSerializer(data=request.data)
        if not serializer.is_valid():
            logger.error('Failed to create Purchase: %s', serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        validated_data = serializer.validated_data
        details_data = validated_data.get('details')

        try:
            with transaction.atomic():

                datos_creacion = {'supplierfk_id': validated_data.get('supplier_id')
                }
                if 'datePurchase' in validated_data:
                    datos_creacion['datePurchase'] = validated_data['datePurchase']

                #Creando el objeto de la compra principal
                new_purchase = purchase_product.objects.create(**datos_creacion)

                total_purchaseCalculated = 0

                #Iterar sobre los detalles de la compra para crear los registros  y actualizar el stock del producto
                for details_item in details_data:
                    productID = details_item['productID']
                    quantity_Purchased = details_item['quantity']
                    unit_cost = details_item['unit_cost']

                    Product_obj = product.objects.select_for_update().get(idProduct=productID)

                    #Estableciendo la lógica del negocio sobre aumentar el stock del producto
                    Product_obj.current_stock += quantity_Purchased

                    #Actualizar el precio de costo del producto al más reciente en los registros
                    Product_obj.price_cost = unit_cost
                    Product_obj.save()

                    #Crear el registro de los detalles de compra (Detail_Purchase) automaticamente
                    detail_purchase.objects.create(
                        purchaseFK = new_purchase,
                        productfk = Product_obj,
                        quantity = quantity_Purchased,
                        unit_cost = unit_cost,
                    )
                    total_purchaseCalculated += quantity_Purchased * unit_cost

                #Actualizar el total de la compra principal
                new_purchase.total_purchase = round(total_purchaseCalculated, 2)
                new_purchase.save()

                #Devolver la compra recien creada y serializada para confirmar el registro
                responsePurchase_serializer = PurchaseSerializer(new_purchase)
                logger.info('Purchase created successfully')
                return Response(responsePurchase_serializer.data, status=status.HTTP_201_CREATED)

        except product.DoesNotExist:
            return Response({"error": "Uno de los productos en la compra no ha sido encontrado"}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return Response({"error": f"Ocurrio un error inesperado: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)