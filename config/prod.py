from .settings import *
import os

# --- CONFIGURACIÓN DE PRODUCCIÓN ---__
SECRET_KEY = os.environ.get('SECRET_KEY')
DEBUG = False
ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', '').split(',')

# Para que Django sepa que está detrás de un proxy seguro (HTTPS en Azure)
# y genere las URLs correctamente.
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_SSL_REDIRECT = True

DATABASES = {
    'default': {
        'ENGINE': 'mssql',
        'NAME': os.environ.get('DBA_NAME'),
        'USER': os.environ.get('DBA_USER'),
        'PASSWORD': os.environ.get('PASSWORD'),
        'HOST': os.environ.get('DBA_HOST'),
        'PORT': '1433',
        'OPTIONS': {
            'driver': 'ODBC Driver 17 for SQL Server',
            'extra_params': 'Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30',
        }
    },
    'data_warehouse': {
        'ENGINE': 'mssql',
        'NAME': os.environ.get('DB_NAME_DW'),
        'USER': os.environ.get('DB_USER_DW'),
        'PASSWORD': os.environ.get('DB_PASSWORD_DW'),
        'HOST': os.environ.get('DB_HOST_DW'),
        'PORT': '1433',
        'OPTIONS': {
            'driver': 'ODBC Driver 17 for SQL Server',
            'extra_params': 'Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30',
        }
    },
}

# config/prod.py
CORS_ALLOWED_ORIGINS = os.environ.get('CORS_ALLOWED_ORIGINS', '').split(',')