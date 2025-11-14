from pymongo import MongoClient
from decouple import config
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

#Conectar con Cosmos DB para realizar una consulta para listar los productos
class ReporteListaPrductosApiView(APIView):
    """
    Endpoint que consume Cosmos DB para listar todos los productos
    con sus categorias y proveedores
    """
    def get (self, request, *args, **kwargs):
        try:
            cosmos_url = config('COSMOS_CONNECTION_STRING')
            client = MongoClient(cosmos_url)
            db = client['FactuSoftDB_mongo']

            #Pipeline de agregación para Listar productos
            pipeline = [
                {
                    '$lookup': {
                    'from': "Product_Category",
                    'localField': "categoryfk_id",
                    'foreignField': "idCategory",
                    'as': "datos_categoria"
                    }
                },
                {
                    '$lookup': {
                        'from': "Supplier",
                        'localField': "supplierfk_id",
                        'foreignField': "idSupplier",
                        'as': "datos_proveedor"
                    }
                },
                {'$unwind': "$datos_categoria"},
                {'$unwind': "$datos_proveedor"},
                {
                    '$project': {
                        '_id': 0,
                        'nombre_producto': "$nameProduct",
                        'precio_venta': "$price_selling",
                        'stock': "$current_stock",
                        'categoria': "$datos_categoria.nameCategory",
                        'proveedor': "$datos_proveedor.nameSupplier"
                    }
                },
                {
                    '$sort': {'nombre_producto': 1}
                }
            ]
            #Se ejecutará el Pipeline en la colección Products
            cursor = db.Products.aggregate(pipeline)
            results = list(cursor)
            client.close()

            return Response(results, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {'error': "Error al consultar Cosmos DB", "details":
                    str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)