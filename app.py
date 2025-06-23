# Corrected/Final app.py (Chatbot Route Only Uses Azure SQL)

from flask import Flask, render_template, request
import pyodbc
from datetime import datetime
import os

app = Flask(__name__)

# Function to fetch latest sensor data
def fetch_latest_sensor():
    try:
        conn = pyodbc.connect(
            "DRIVER={ODBC Driver 17 for SQL Server};"
            "SERVER=tdmsql.database.windows.net;"
            "DATABASE=DynamicsByod;"
            "UID=sqladmin;"
            "PWD=tdmtdM@kt;"
            "Encrypt=yes;"
        )
        cursor = conn.cursor()
        cursor.execute("""
            SELECT TOP 10 Temperature, Humidity, Position, Sensor, Date
            FROM Agrobiz.SENSOR_DATA
            ORDER BY Date DESC
        """)
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        return rows
    except Exception as e:
        print("❌ Error while connecting to database or fetching data:", e)
        return None

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
        if rows:
            latest = rows[0]
            max_temp_row = max(rows, key=lambda x: x.Temperature)
            min_hum_row = min(rows, key=lambda x: x.Humidity)
            if "temperature" in msg:
                return f"🌡️ Current temperature is {latest.Temperature}°C at {latest.Position} (Sensor {latest.Sensor}) as of {latest.Date.strftime('%Y-%m-%d')}."
            elif "humidity" in msg:
                return f"💧 Current humidity is {latest.Humidity}% at {latest.Position} (Sensor {latest.Sensor}) as of {latest.Date.strftime('%Y-%m-%d')}."
            elif "water" in msg or "irrigation" in msg or "siram" in msg:
                if latest.Temperature > 30 or latest.Humidity < 50:
                    return f"✅ Yes, watering is advisable (Temp: {latest.Temperature}°C, Humidity: {latest.Humidity}%)."
                else:
                    return f"🚫 No need to water now. (Temp: {latest.Temperature}°C, Humidity: {latest.Humidity}%)."
            elif "hottest" in msg or "highest temperature" in msg:
                return f"🔥 The highest temperature is {max_temp_row.Temperature}°C at {max_temp_row.Position} (Sensor {max_temp_row.Sensor}) on {max_temp_row.Date.strftime('%Y-%m-%d')}."
            elif "lowest humidity" in msg or "driest" in msg:
                return f"💨 The lowest humidity is {min_hum_row.Humidity}% at {min_hum_row.Position} (Sensor {min_hum_row.Sensor}) on {min_hum_row.Date.strftime('%Y-%m-%d')}."
            else:
                return "❓ Sorry, I can only answer questions about temperature, humidity, or irrigation right now."
        else:
            return "⚠️ No sensor data found in the database."
    except Exception as e:
        print("❌ Server error:", e)
        return f"⚠️ Server error: {str(e)}"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
