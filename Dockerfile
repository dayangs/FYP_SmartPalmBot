FROM python:3.10-slim

# Install ODBC Driver 18 for SQL Server and dependencies
RUN apt-get update && \
    apt-get install -y curl gnupg unixodbc-dev && \
    curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add - && \
    curl https://packages.microsoft.com/config/ubuntu/22.04/prod.list > /etc/apt/sources.list.d/mssql-release.list && \
    apt-get update && \
    ACCEPT_EULA=Y apt-get install -y msodbcsql18

# Set the working directory
WORKDIR /app

# Copy all your code to the container
COPY . .

# Install Python requirements
RUN pip install --upgrade pip && pip install -r requirements.txt

# Expose your app's port (optional, for clarity)
EXPOSE 10000

# Start the app with Gunicorn (production-ready)
CMD ["gunicorn", "app:app"]
