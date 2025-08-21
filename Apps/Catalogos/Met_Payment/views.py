from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics, filters

from config.utils.Pagination import PaginationMixin
from .models import metPayment
from .serializers import metPaymentSerializer
from drf_yasg.utils import swagger_auto_schema

from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated

from ...permissions import CustomPermission
from config.utils.Pagination import PaginationMixin
import logging.handlers

# Configuracion de el logger
logger = logging.getLogger(__name__)

class metPaymentApiview(PaginationMixin,APIView):
    #permission_classes = [CustomPermission]
    model = metPayment

    @swagger_auto_schema(responses={200: metPaymentSerializer(many=True)})
    def get(self,request):

        """""
        Obtener todas las formas de pago
        """
        logger.info('GET request to list all Method Payments')
        method_payments = metPayment.objects.all().order_by('idPayment')
        page = self.paginate_queryset(method_payments, request)

        if page is not None:
            serializer = metPaymentSerializer(page, many=True)
            logger.info('Paginated response for method payments')
            return self.get_paginated_response(serializer.data)

        serializer = metPaymentSerializer(method_payments, many=True)
        logger.error('Returning all method payments without a page')
        return Response(serializer.data)

    @swagger_auto_schema(request_body=metPaymentSerializer,responses={200: metPaymentSerializer(many=True)})
    def post(self, request):
        """"
        Ingresar un método de pago nuevo
        """
        logger.info('POST request to list all Method Payments')
        serializer = metPaymentSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            logger.info('method payment created successfully')
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        logger.error('Failed to create Method payment: %s', serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class metPayment_PPD_Apiview(PaginationMixin,APIView):
    #permission_classes = [CustomPermission]
    model = metPayment

    @swagger_auto_schema(request_body=metPaymentSerializer,responses={200: metPaymentSerializer(many=True)})
    def put(self,request, pk):
        """
        Actualizar totalmente un método de pago
        """
        logger.info('PUT request to list all Method Payments')
        method_payment = get_object_or_404(metPayment, idPayment=pk)
        if not method_payment:
            return Response({'error': 'Método de pago no encontrado'}, status=status.HTTP_404_NOT_FOUND)

        self.check_object_permissions(request, method_payment)
        serializer = metPaymentSerializer(method_payment,data=request.data)
        if serializer.is_valid():
            serializer.save()
            logger.info('Method payment updated successfully with ID: %s', pk)
            return Response(serializer.data)
        logger.error('Failed to update Method payment with ID: %s. Errors: %s',pk, serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(request_body=metPaymentSerializer,responses={200: metPaymentSerializer(many=True)})
    def patch(self,request,pk):
        """Actualizar parcialmente un método de pago"""
        logger.info('PATCH request to partially update Method Payments with ID: %s', pk)
        method_payment = get_object_or_404(metPayment, idPayment=pk)
        if not method_payment:
            return Response({'error': 'Método de pago no encontrado'}, status=status.HTTP_404_NOT_FOUND)
        self.check_object_permissions(request, method_payment)
        serializer = metPaymentSerializer(method_payment,data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            logger.info('Method payment partially updated successfully with ID: %s', pk)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(responses={204: 'No Content'})
    def delete(self,request,pk):
        """Eliminar un método de pago"""
        logger.info('DELETE request to delete Method Payments with ID: %s', pk)
        method_payment = get_object_or_404(metPayment, idPayment=pk)
        if not method_payment:
            return Response({'error': 'Método de pago no encontrado'}, status=status.HTTP_404_NOT_FOUND)

        self.check_object_permissions(request, method_payment)
        method_payment.delete()
        logger.info('Method payment deleted successfully with ID: %s', pk)
        return Response(status=status.HTTP_204_NO_CONTENT)