from pymongo import MongoClient
from decouple import config
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

#Conectar con Cosmos DB para realizar una consulta para listar los productos
class ReporteDetallarVentaApiView(APIView):
    """
        Endpoint que consume Cosmos DB para obtener el detalle 
        completo de una venta en especifica
    """

    def get(self, request, id_venta, *args, **kwargs):
        try:
            cosmos_url = config('COSMOS_CONNECTION_STRING')
            client = MongoClient(cosmos_url)
            db = client['FactuSoftDB_mongo']

            # Pipeline de Agregación para "Detalle de Venta"
            pipeline = [
                {

                    '$match': {'idSalesProduct': id_venta}
                },
                {
                    '$lookup': {
                        'from': "customers",
                        'localField': "customerFk_id",
                        'foreignField': "idCustomer",
                        'as': "datos_client"
                    }
                },
                {
                    '$lookup': {
                        'from': "Users",
                        'localField': "user_id",
                        'foreignField': "id",
                        'as': "datos_usuario"
                    },
                },
                {
                    '$lookup': {
                        'from': "DetailSales",
                        'localField': "idSalesProduct",
                        'foreignField': "saleFk_id",
                        'as': "items_vendidos"
                    },
                },
                {
                    '$unwind': "$items_vendidos"
                },
                {
                    '$lookup': {
                        'from': "Products",
                        'localField': "items_vendidos.productFK_id",
                        'foreignField': "idProduct",
                        'as': "detalles_producto"
                    },
                },
                {
                    '$group': {
                        '_id': "$_id",
                        'idSalesProduct': {'$first': "$idSalesProduct"},
                        'dateSales': {'$first': "$dateSales"},
                        'total_sales': {'$first': "$total_sales"},
                        'cliente': {'$first': "$datos_client"},
                        'vendedor': {'$first': "$datos_usuario"},
                        'productos': {
                            '$push': {
                                'nombre': {'$arrayElemAt': ["$detalles_producto.nameProduct", 0]},
                                'cantidad': "$items_vendidos.quantity_detailSales",
                                'precio_unitario': "$items_vendidos.price_Unit"
                            }
                        }
                    }
                },
                {

                    '$project': {
                        '_id': 0,
                        'factura_id': "$idSalesProduct",
                        'fecha': "$dateSales",
                        'total': "$total_sales",
                        'cliente': {
                            'nombre': { '$arrayElemAt': ["$cliente.CustName", 0] },
                            'apellido': {'$arrayElemAt': ["$cliente.CustLastName", 0]},
                            'email': { '$arrayElemAt': ["$cliente.email", 0] }
                        },
                        'vendedor': {
                            'nombre_usuario': {'$arrayElemAt': ["$vendedor.username", 0]},
                            'nombre_completo': {
                                '$concat': [
                                    {'$arrayElemAt': ["$vendedor.first_name", 0]},
                                    " ",
                                    {'$arrayElemAt': ["$vendedor.last_name", 0]}
                                ]
                            }
                        },
                        'productos_vendidos': "$productos"
                    }
                }
            ]
            #Se ejecutará el pipeline en la coleccion Sales_product
            cursor = db.Sales_product.aggregate(pipeline)
            results = list(cursor)
            client.close()

            #Si la consulta no devuelve nada en caso de que algun id de venta no existe
            if not results:
                return Response(
                    {"error": f"Venta con ID {id_venta} no encontrada"},
                    status=status.HTTP_404_NOT_FOUND
                )

            #Se devuelve el primer y unico documento de la lista
            return Response(results[0], status=status.HTTP_200_OK)

        except Exception as e:
            return Response(
                {"error": "Error al consultar Cosmos DB", "details": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
