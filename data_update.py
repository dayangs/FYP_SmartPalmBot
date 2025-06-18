import logging
import pandas as pd
from datetime import datetime
import smtplib
from email.message import EmailMessage
import ssl
import pyodbc

# Email notification setup
def send_email(subject, body):
    from_email = 'dygnadirah02@gmail.com'
    to_email = 'senjagunung01@gmail.com'
    password = 'boeh xacy kwgl ggwf' # App password for Gmail
    
    em = EmailMessage()
    em['From'] = from_email
    em['To'] = to_email
    em['Subject'] = subject
    em.set_content(body)

    context = ssl.create_default_context()

    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
            smtp.starttls(context=context)
            smtp.login(from_email, password)
            smtp.send_message(em)
        logging.info("Email sent successfully.")
    except Exception as e:
        logging.error("Error while sending email: %s", e)

# Main function to process and update data
def main():

    # CSV file path
    csv_path = r'C:\Users\ACER\Desktop\unimas\TMF4913 FYP\Analysis Dashboard\Sensor Data\SENSOR_DATA.csv'

    # Load CSV and preprocessing
    df = pd.read_csv(csv_path)
    df['Date'] = pd.to_datetime(df['Date'], dayfirst=True, errors='coerce').dt.date
    df['Time'] = df['Time'].astype(str)
    df['Temperature'] = pd.to_numeric(df['Temperature'], errors='coerce').round(1)
    df['Humidity'] = pd.to_numeric(df['Humidity'], errors='coerce').astype('Int64')
    df['Sensor'] = pd.to_numeric(df['Sensor'], errors='coerce').astype('Int64')
    df['Temperature_Abnormal'] = df['Temperature_Abnormal'].astype(str)
    df['Humidity_Abnormal'] = df['Humidity_Abnormal'].astype(str)
    df['Position'] = df['Position'].astype(str)
    df.dropna(subset=['Date', 'Time', 'Temperature', 'Humidity', 'Sensor'], inplace=True)

     # Database credentials
    username = 'sqladmin'
    password = 'tdmtdM@kt'
    server = 'tdmsql.database.windows.net'
    database = 'DynamicsByod'

    # Connection string
    connection_string = (
        'DRIVER={ODBC Driver 17 for SQL Server};'
        'SERVER=' + server + ';'
        'DATABASE=' + database + ';'
        'UID=' + username + ';'
        'PWD=' + password
    )

    # Establish the connection and insert data
    try:
        connection = pyodbc.connect(connection_string)
        logging.info("Connected to Azure SQL successfully.")
    except pyodbc.Error as e:
        logging.error("Database connection failed: %s", e)
        send_email("Data Update Failed", f"Database connection error: {e}")
        return

    new_entries = 0
    try:
        cursor = connection.cursor()

        # Fetch existing keys
        cursor.execute("SELECT CONCAT(Date, '_', Time, '_', Sensor) FROM Agrobiz.SENSOR_DATA")
        existing_keys = set(row[0] for row in cursor.fetchall())
        logging.info("Fetched %d existing keys from DB.", len(existing_keys))

        # Build unique keys for new data
        df['RowKey'] = df.apply(lambda row: f"{row['Date']}_{row['Time']}_{row['Sensor']}", axis=1)
        new_data = df[~df['RowKey'].isin(existing_keys)]
        logging.info("New rows to insert: %d", len(new_data))

        for _, row in new_data.iterrows():
            cursor.execute("""
                INSERT INTO Agrobiz.SENSOR_DATA (Date, Time, Temperature, Temperature_Abnormal,
                                            Humidity, Humidity_Abnormal, Position, Sensor)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, row['Date'], row['Time'], row['Temperature'], row['Temperature_Abnormal'],
                row['Humidity'], row['Humidity_Abnormal'], row['Position'], row['Sensor'])
            new_entries += 1

        # Commit the transaction 
        connection.commit()
        logging.info("Insert complete. Total new entries: %d", new_entries)
        
        # Send email notification
        send_email(
            "Data Update Successful",
            f"{new_entries} new sensor readings inserted into the database successfully."
        )

    except Exception as e:
        logging.error("Error inserting data: %s", e)
        send_email("Tapo Data Update Failed", f"Error inserting data: {e}")

    finally:
        try:
            connection.close()
            logging.info("Database connection closed.")
        except:
            pass

if __name__ == "__main__":
    main()
