from flask import Flask, render_template, request
import pyodbc
from decimal import Decimal
import datetime
import os

app = Flask(__name__)

def fetch_latest_sensor():
    try:
        conn = pyodbc.connect(
            "DRIVER={ODBC Driver 18 for SQL Server};"
            "SERVER=tdmsql.database.windows.net;"
            "DATABASE=DynamicsByod;"
            "UID=sqladmin;"
            "PWD=tdmtdM@kt;"
            "Encrypt=yes;"
        )
        cursor = conn.cursor()
        cursor.execute("""
            SELECT TOP 10 Temperature, Humidity, Position, Sensor, Date, Time
            FROM Agrobiz.SENSOR_DATA
            ORDER BY Date DESC, Time DESC
        """)
        columns = [column[0] for column in cursor.description]
        rows = [dict(zip(columns, row)) for row in cursor.fetchall()]
        print(f"[DEBUG] Number of rows fetched: {len(rows)}")
        if rows:
            print("[DEBUG] Sample row:", rows[0])
        else:
            print("[DEBUG] No data returned from SQL query.")
        cursor.close()
        conn.close()
        return rows
    except Exception as e:
        print("❌ Error while connecting to database or fetching data:", e)
        return None

def parse_value(val):
    if isinstance(val, Decimal):
        return float(val)
    if isinstance(val, datetime.date):
        return val.strftime("%Y-%m-%d")
    return str(val)

def row_display(row):
    # Convert every value to a Python-native type
    return {k: parse_value(v) for k, v in row.items()}

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat")
def chat():
    return render_template("chat.html")

@app.route("/get", methods=["POST"])
def chatbot_response():
    try:
        msg = request.form["msg"].lower()
        rows = fetch_latest_sensor()
        print("[DEBUG] /get endpoint rows:", rows)  # <--- ADDED
        if rows and len(rows) > 0:
            parsed_rows = [row_display(r) for r in rows]
            latest = parsed_rows[0]
            max_temp_row = max(parsed_rows, key=lambda x: x["Temperature"])
            min_hum_row = min(parsed_rows, key=lambda x: x["Humidity"])

            if "temperature" in msg:
                return f"🌡️ Current temperature is {latest['Temperature']}°C at {latest['Position']} (Sensor {latest['Sensor']}) as of {latest['Date']} {latest['Time']}."
            elif "humidity" in msg:
                return f"💧 Current humidity is {latest['Humidity']}% at {latest['Position']} (Sensor {latest['Sensor']}) as of {latest['Date']} {latest['Time']}."
            elif "water" in msg or "irrigation" in msg or "siram" in msg:
                if latest['Temperature'] > 30 or latest['Humidity'] < 50:
                    return f"✅ Yes, watering is advisable (Temp: {latest['Temperature']}°C, Humidity: {latest['Humidity']}%)."
                else:
                    return f"🚫 No need to water now. (Temp: {latest['Temperature']}°C, Humidity: {latest['Humidity']}%)."
            elif "hottest" in msg or "highest temperature" in msg:
                return f"🔥 The highest temperature is {max_temp_row['Temperature']}°C at {max_temp_row['Position']} (Sensor {max_temp_row['Sensor']}) on {max_temp_row['Date']} at {max_temp_row['Time']}."
            elif "lowest humidity" in msg or "driest" in msg:
                return f"💨 The lowest humidity is {min_hum_row['Humidity']}% at {min_hum_row['Position']} (Sensor {min_hum_row['Sensor']}) on {min_hum_row['Date']} at {min_hum_row['Time']}."
            else:
                return "❓ Sorry, I can only answer questions about temperature, humidity, or irrigation right now."
        else:
            print("[DEBUG] No rows found or rows is None")
            return "⚠️ No sensor data found in the database."
    except Exception as e:
        print("❌ Server error in /get:", e)
        return f"⚠️ Server error: {str(e)}"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
