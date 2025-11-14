#!/bin/bash
export DEBIAN_FRONTEND=noninteractive

# Añadir el repositorio de Microsoft
curl -sSL https://packages.microsoft.com/keys/microsoft.asc | apt-key add -
curl -sSL https://packages.microsoft.com/config/debian/11/prod.list -o /etc/apt/sources.list.d/mssql-release.list

# Instalar el driver
apt-get update
ACCEPT_EULA=Y apt-get install -y msodbcsql17 unixodbc-dev