from flask import Flask, render_template, request
import pyodbc
import os

app = Flask(__name__)

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
            SELECT TOP 10 Temperature, Humidity, Position, Sensor, Date, Time
            FROM Agrobiz.SENSOR_DATA
            ORDER BY Date DESC, Time DESC
        """)
        columns = [column[0] for column in cursor.description]
        rows = [dict(zip(columns, row)) for row in cursor.fetchall()]
        cursor.close()
        conn.close()
        print(f"Fetched {len(rows)} rows.")
        if rows:
            print("Sample row:", rows[0])
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
            # Safely handle potential non-numeric data:
            try:
                max_temp_row = max(rows, key=lambda x: float(x["Temperature"]))
            except Exception:
                max_temp_row = latest
            try:
                min_hum_row = min(rows, key=lambda x: float(x["Humidity"]))
            except Exception:
                min_hum_row = latest

            if "temperature" in msg:
                return f"🌡️ Current temperature is {latest['Temperature']}°C at {latest['Position']} (Sensor {latest['Sensor']}) as of {latest['Date']} {latest['Time']}."
            elif "humidity" in msg:
                return f"💧 Current humidity is {latest['Humidity']}% at {latest['Position']} (Sensor {latest['Sensor']}) as of {latest['Date']} {latest['Time']}."
            elif "water" in msg or "irrigation" in msg or "siram" in msg:
                temp = float(latest['Temperature']) if latest['Temperature'] else 0
                hum = float(latest['Humidity']) if latest['Humidity'] else 0
                if temp > 30 or hum < 50:
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
            return "⚠️ No sensor data found in the database."
    except Exception as e:
        print("❌ Server error:", e)
        return f"⚠️ Server error: {str(e)}"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
