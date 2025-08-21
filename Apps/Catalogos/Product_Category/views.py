from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from config.utils.Pagination import PaginationMixin
from .models import product_Category
from .serializers import ProductCategorySerializer
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

# Vista para Listar todos las categorias y Crear uno nuevo
class CategoryListCreateAPIView(APIView, PaginationMixin):
    # permission_classes = [IsAuthenticated]

    @swagger_auto_schema(responses={200: ProductCategorySerializer(many=True)})
    def get(self, request):

        """Obtener el listado paginado de todas las Categorias.
        """
        logger.info("GET request to list all Product Category")
        queryset = product_Category.objects.all().order_by('idCategory')
        page = self.paginate_queryset(queryset, request)
        if page is not None:
            serializer = ProductCategorySerializer(page, many=True)
            logger.info("Paginated response for Product Category List")
            return self.get_paginated_response(serializer.data)

        serializer = ProductCategorySerializer(queryset, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(request_body=ProductCategorySerializer, responses={201: ProductCategorySerializer()})
    def post(self, request):
        """Ingresar una categoria nueva."""
        logger.info("POST request to create a new Product Category")
        serializer = ProductCategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            logger.info("Product Category created successfully")
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        logger.error("Failed to create Product Category: %s", serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Vista para manejar una sola categoria por su ID
class CategoryDetailAPIView(APIView):
    # permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        """
        Helper para obtener el objeto o devolver un 404.

        """
        try:
            return product_Category.objects.get(idCategory=pk)
        except product_Category.DoesNotExist:
            raise Http404

    @swagger_auto_schema(responses={200: ProductCategorySerializer()})
    def get(self, request, pk):
        """Obtener los detalles de una categoria específico."""
        category_obj = self.get_object(pk)
        serializer = ProductCategorySerializer(category_obj)
        return Response(serializer.data)

    @swagger_auto_schema(request_body=ProductCategorySerializer, responses={200: ProductCategorySerializer()})
    def put(self, request, pk):
        """Actualizar totalmente una categoria."""
        category_obj = self.get_object(pk)
        serializer = ProductCategorySerializer(category_obj, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(request_body=ProductCategorySerializer, responses={200: ProductCategorySerializer()})
    def patch(self, request, pk):
        """Actualizar parcialmente una categoria."""
        category_obj = self.get_object(pk)
        serializer = ProductCategorySerializer(category_obj, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(responses={204: 'No Content'})
    def delete(self, request, pk):
        """Eliminar una categoria."""
        category_obj = self.get_object(pk)
        category_obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)