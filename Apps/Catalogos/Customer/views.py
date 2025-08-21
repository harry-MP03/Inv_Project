from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from config.utils.Pagination import PaginationMixin
from .models import customer
from .serializers import CustomerSerializer
from drf_yasg.utils import swagger_auto_schema
from django.http import Http404

from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated

from ...permissions import CustomPermission
from config.utils.Pagination import PaginationMixin
import logging.handlers

# Configuracion de el logger
logger = logging.getLogger(__name__)

# Vista para LISTAR todos los clientes y CREAR uno nuevo
class CustomerListCreateAPIView(APIView, PaginationMixin):
    # permission_classes = [IsAuthenticated]

    @swagger_auto_schema(responses={200: CustomerSerializer(many=True)})
    def get(self, request):
        """Obtener el listado paginado de todos los clientes."""
        logger.info("GET request to list all customers")
        queryset = customer.objects.all().order_by('idCustomer')
        page = self.paginate_queryset(queryset, request)
        if page is not None:
            serializer = CustomerSerializer(page, many=True)
            logger.info("Paginated response for Customers List")
            return self.get_paginated_response(serializer.data)

        serializer = CustomerSerializer(queryset, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(request_body=CustomerSerializer, responses={201: CustomerSerializer()})
    def post(self, request):
        """Ingresar un cliente nuevo."""
        logger.info("POST request to create a new Customer")
        serializer = CustomerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            logger.info("Customer created successfully")
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        logger.error("Failed to create Customer: %s", serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Vista para manejar un solo cliente por su ID
class CustomerDetailAPIView(APIView):
    # permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        """
        Helper para obtener el objeto o devolver un 404.

        """
        try:
            return customer.objects.get(idCustomer=pk)
        except customer.DoesNotExist:
            raise Http404

    @swagger_auto_schema(responses={200: CustomerSerializer()})
    def get(self, request, pk):
        """Obtener los detalles de un cliente específico."""
        customer_obj = self.get_object(pk)
        serializer = CustomerSerializer(customer_obj)
        return Response(serializer.data)

    @swagger_auto_schema(request_body=CustomerSerializer, responses={200: CustomerSerializer()})
    def put(self, request, pk):
        """Actualizar totalmente un cliente."""
        customer_obj = self.get_object(pk)
        serializer = CustomerSerializer(customer_obj, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(request_body=CustomerSerializer, responses={200: CustomerSerializer()})
    def patch(self, request, pk):
        """Actualizar parcialmente un cliente."""
        customer_obj = self.get_object(pk)
        serializer = CustomerSerializer(customer_obj, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(responses={204: 'No Content'})
    def delete(self, request, pk):
        """Eliminar un cliente."""
        customer_obj = self.get_object(pk)
        customer_obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)