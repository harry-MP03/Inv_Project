from django.db import connections
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

def dictfetchall(cursor):
    """
    Convirtiendo todas las filas de un cursor como diccionario
    esta funcion tiene como objetivo convertir los datos de SQL a JSON
    :param cursor:
    :return:
    """
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]

class ReporteVentasCategoriaApiView(APIView):
    """
    Endpoint de un reporte de ventas por categoria consumiendo desde el DW
    """
    def get(self, request, *args, **kwargs):
        #1. La consulta a la Vista (Views) que se ha creado en SQL
        query = """
            SELECT Categoria, TotalLinea
            FROM vista_reporte_VentasPorCategoria_2025
            ORDER BY TotalLinea DESC
            """
        try:
            #2. Se conecta a la BD 'data_warehouse'
            with connections['data_warehouse'].cursor() as cursor:
                cursor.execute(query)
                results = dictfetchall(cursor) #Se utiliza la funcion previa

            #3. Se devuelve los resultados como JSON
            return Response(results, status=status.HTTP_200_OK)

        except Exception as e:
            #Se captura cualquier error de la base de datos
            return Response(
                {"error": "Error al consultar el DataWarehouse.", "detail": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )