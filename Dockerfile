FROM python:3.10-slim

# Install ODBC Driver for SQL Server and dependencies
RUN apt-get update && \
    apt-get install -y curl gnupg unixodbc-dev && \
    curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add - && \
    curl https://packages.microsoft.com/config/ubuntu/22.04/prod.list > /etc/apt/sources.list.d/mssql-release.list && \
    apt-get update && \
    ACCEPT_EULA=Y apt-get install -y msodbcsql18

WORKDIR /app

COPY . .

RUN pip install --upgrade pip && pip install -r requirements.txt

EXPOSE 10000

# Start the app
CMD ["gunicorn", "app:app", "--bind", "0.0.0.0:10000"]
