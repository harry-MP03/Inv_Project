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
class VentasMensualesGeneralApiView(APIView):
    """
    Endpoint para obtener la cronologia de ventas totales por mes
    """
    def get(self, request, *args, **kwargs):
        #1. Consulta a la Vista (View)
        #Seleccionar las columnas que se quieran mostrar
        #Ordenar por Anio y Numero del Mes (Mes) para la cronologia correcta
        query = """
        SELECT Anio, NombreMes, TotalVentas
        FROM vista_Reporte_VentasMensuales
        WHERE Anio = 2025
        ORDER BY Mes;
        """

        try:
            #2.Conectarse a la BD data_warehouse
            with connections['data_warehouse'].cursor() as cursor:
                cursor.execute(query)
                results = dictfetchall(cursor)
            #Se devuelve en formato JSON
            return Response(results, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {'error': "Error al consultar el Data Warehouse", "details": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR)