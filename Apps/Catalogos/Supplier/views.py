from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from config.utils.Pagination import PaginationMixin
from .models import supplier
from .serializers import supplierSerializer
from drf_yasg.utils import swagger_auto_schema
from django.http import Http404

from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated

from .. import Customer
from ...permissions import CustomPermission
from config.utils.Pagination import PaginationMixin
import logging.handlers

# Configuracion de el logger
logger = logging.getLogger(__name__)

# Vista para listar todos los proveedores y crear uno nuevo
class SupplierListCreateAPIView(APIView, PaginationMixin):
    # permission_classes = [IsAuthenticated]

    @swagger_auto_schema(responses={200: supplierSerializer(many=True)})
    def get(self, request):
        """Obtener el listado paginado de todos los Proveedores."""
        logger.info("GET request to list all suppliers")
        queryset = supplier.objects.all().order_by('idSupplier')
        page = self.paginate_queryset(queryset, request)
        if page is not None:
            serializer = supplierSerializer(page, many=True)
            logger.info("Paginated response for Suppliers List")
            return self.get_paginated_response(serializer.data)

        serializer = supplierSerializer(queryset, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(request_body=supplierSerializer, responses={201: supplierSerializer()})
    def post(self, request):
        """Ingresar un proveedor nuevo."""
        logger.info("POST request to create a new supplier")
        serializer = supplierSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            logger.info("Supplier created successfully")
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        logger.error("Failed to create Supplier: %s", serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Vista para manejar un solo proveedor por su ID
class SupplierDetailAPIView(APIView):
    # permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        """
        Helper para obtener el objeto o devolver un 404.

        """
        try:
            return supplier.objects.get(idSupplier=pk)
        except supplier.DoesNotExist:
            raise Http404

    @swagger_auto_schema(responses={200: supplierSerializer()})
    def get(self, request, pk):
        """Obtener los detalles de un proveedor específico."""
        supplier_obj = self.get_object(pk)
        serializer = supplierSerializer(supplier_obj)
        return Response(serializer.data)

    @swagger_auto_schema(request_body=supplierSerializer, responses={200: supplierSerializer()})
    def put(self, request, pk):
        """Actualizar totalmente un proveedor."""
        supplier_obj = self.get_object(pk)
        serializer = supplierSerializer(supplier_obj, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(request_body=supplierSerializer, responses={200: supplierSerializer()})
    def patch(self, request, pk):
        """Actualizar parcialmente un Proveedor."""
        supplier_obj = self.get_object(pk)
        serializer = supplierSerializer(supplier_obj, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(responses={204: 'No Content'})
    def delete(self, request, pk):
        """Eliminar un proveedor."""
        supplier_obj = self.get_object(pk)
        supplier_obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
