from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from config.utils.Pagination import PaginationMixin
from .models import product
from .serializers import productReadDetail_Serializer, productSerializer
from drf_yasg.utils import swagger_auto_schema
from django.http import Http404

from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated

from ...permissions import CustomPermission
from config.utils.Pagination import PaginationMixin
import logging.handlers

# Configuracion de el logger
logger = logging.getLogger(__name__)

# Vista para listar todos los productos y crear uno nuevo
class ProductListCreateAPIView(APIView, PaginationMixin):
    # permission_classes = [IsAuthenticated]

    @swagger_auto_schema(responses={200: productReadDetail_Serializer(many=True)})
    def get(self, request):
        """Obtener el listado paginado de todos los productos."""
        logger.info("GET request to list all products")
        queryset = product.objects.all().order_by('idProduct')
        page = self.paginate_queryset(queryset, request)
        if page is not None:
            serializer = productReadDetail_Serializer(page, many=True)
            logger.info("Paginated response for Products List")
            return self.get_paginated_response(serializer.data)

        serializer = productReadDetail_Serializer(queryset, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(request_body=productSerializer, responses={201: productSerializer()})
    def post(self, request):
        """Ingresar un producto nuevo."""
        logger.info("POST request to create a new Product")
        serializer = productSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            logger.info("Product created successfully")
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        logger.error("Failed to create Product: %s", serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Vista para manejar un solo producto por su ID
class ProductDetailAPIView(APIView):
    # permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        """
        Helper para obtener el objeto o devolver un 404.

        """
        try:
            return product.objects.get(idProduct=pk)
        except product.DoesNotExist:
            raise Http404

    @swagger_auto_schema(responses={200: productReadDetail_Serializer()})
    def get(self, request, pk):
        """Obtener los detalles de un Producto específico."""
        product_obj = self.get_object(pk)
        serializer = productReadDetail_Serializer(product_obj)
        return Response(serializer.data)

    @swagger_auto_schema(request_body=productSerializer, responses={200: productSerializer()})
    def put(self, request, pk):
        """Actualizar totalmente un producto."""
        product_obj = self.get_object(pk)
        serializer = productSerializer(product_obj, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(request_body=productSerializer, responses={200: productSerializer()})
    def patch(self, request, pk):
        """Actualizar parcialmente un producto."""
        product_obj = self.get_object(pk)
        serializer = productSerializer(product_obj, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(responses={204: 'No Content'})
    def delete(self, request, pk):
        """Eliminar un producto."""
        producto_obj = self.get_object(pk)
        producto_obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
