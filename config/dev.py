from .settings import *
from decouple import config
from config.utils.logging_config import ANSIColorFormatter

DEBUG = True

ALLOWED_HOSTS = ['127.0.0.1', 'localhost']

SECRET_KEY = config('SECRET_KEY')

DATABASES = {
    'default': {
        'ENGINE': 'mssql',  # Utilizamos el backend mssql-django
        'NAME': config('DBA_NAME'),  # Nombre de la base de datos
        'USER': config('USER'),
        'PASSWORD': config('PASSWORD'),
        'HOST': config('DBA_HOST'),  # IP del servidor SQL Server
        'OPTIONS': {
            'driver': 'ODBC Driver 17 for SQL Server',  # Driver ODBC instalado
            #'trusted_connection': 'yes',  # Habilita la autenticación de Windows
            #'extra_params': 'TrustServerCertificate=yes',  # Útil si estás usando SSL sin un certificado de confianza
            'extra_params': 'Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30',
        },
    },
    #Conexión 2: Data Warehouse
    'data_warehouse': {
        'ENGINE': 'mssql',  # Utilizamos el backend mssql-django
        'NAME': config('DB_NAME_DW'),  # Nombre de la base de datos
        'USER': config('DB_USER_DW'),
        'PASSWORD': config('DB_PASSWORD_DW'),
        'HOST': config('DB_HOST_DW'),  # IP del servidor SQL Server
        'OPTIONS': {
            'driver': 'ODBC Driver 17 for SQL Server',  # Driver ODBC instalado
            #'trusted_connection': 'yes',  # Habilita la autenticación de Windows
            #'extra_params': 'TrustServerCertificate=yes',  # Útil si estás usando SSL sin un certificado de confianza
            'extra_params': 'Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30',
        },
    },
}

