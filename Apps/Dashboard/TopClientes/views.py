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

class ReporteTopClientesApiview(APIView):
    """
    Endpoint para obtener el reporte de top 5 clientes por gasto total
    """

    def get(self, request, *args, **kwargs):
        #1. La consulta a la vista o views ademas de listar en 5 clientes con mas gastos y en orden
        query = """
            SELECT TOP 5 Nombre, TotalGasto
            FROM vista_Reporte_GastoTotalPorCliente
            ORDER BY TotalGasto DESC
            """

        try:
            #2. Se conecta a la BD data_warehouse
            with connections['data_warehouse'].cursor() as cursor:
                cursor.execute(query)
                #Se usa la función de convertir a JSON
                results = dictfetchall(cursor)

            #3. Devolvemos los resultados como JSON
            return Response(results, status=status.HTTP_200_OK)

        except Exception as e:
            #Capturar cualquier error
            return Response(
                {'error': "Error al consultar el Data Warehouse", "details": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR)