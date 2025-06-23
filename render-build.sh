#!/usr/bin/env bash

# Install Microsoft ODBC Driver for SQL Server on Linux (Ubuntu)
curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add -
curl https://packages.microsoft.com/config/ubuntu/22.04/prod.list > /etc/apt/sources.list.d/mssql-release.list
apt-get update
ACCEPT_EULA=Y apt-get install -y msodbcsql18
apt-get install -y unixodbc-dev

# Then install python deps
pip install -r requirements.txt
