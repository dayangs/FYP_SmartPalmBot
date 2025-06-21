from flask import Flask, render_template, request
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch
import pyodbc
from datetime import datetime
import os
import gc

app = Flask(__name__)

def load_model():
    from transformers import AutoModelForCausalLM, AutoTokenizer
    model_dir = "./pretrained/dialo"
    print("Loading model from:", model_dir)
    print("Model directory exists:", os.path.exists(model_dir))
    print("Model directory contents:", os.listdir(model_dir) if os.path.exists(model_dir) else "Missing!")
    tokenizer = AutoTokenizer.from_pretrained(model_dir, local_files_only=True)
    model = AutoModelForCausalLM.from_pretrained(model_dir, local_files_only=True)
    return tokenizer, model

# Keep track of conversation history
chat_history_ids = None

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

        if rows:
            print(f"✅ Database connected. Retrieved {len(rows)} rows.")
        else:
            print("⚠️ Database connected, but no rows returned.")

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

@app.route("/check-model")
def check_model():
    model_dir = "./pretrained/dialo"
    try:
        files = os.listdir(model_dir)
        return "<br>".join(files)
    except Exception as e:
        return f"Error: {e}"

@app.route("/get", methods=["POST"])
def chatbot_response():
    global chat_history_ids
    print("POST /get received")
    msg = request.form["msg"].lower()
    print("User message:", msg)
    rows = fetch_latest_sensor()
    print("Database fetch result:", rows)

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
        
    # Fallback to DialoGPT response
    try:
        print("🧠 Falling back to DialoGPT...")
        tokenizer, model = load_model()  # <- Lazy load only when needed
        new_input_ids = tokenizer.encode(msg + tokenizer.eos_token, return_tensors='pt')

        if chat_history_ids is not None:
            bot_input_ids = torch.cat([chat_history_ids, new_input_ids], dim=-1)
        else:
            bot_input_ids = new_input_ids

        chat_history_ids = model.generate(
            bot_input_ids,
            max_length=1000,
            pad_token_id=tokenizer.eos_token_id,
            no_repeat_ngram_size=3,
            do_sample=True,
            top_k=100,
            top_p=0.7,
            temperature=0.9,
        )

        reply = tokenizer.decode(chat_history_ids[:, bot_input_ids.shape[-1]:][0], skip_special_tokens=True)
        
        # Cleanup to save memory
        del tokenizer, model
        gc.collect()
        
        print("DialoGPT reply:", reply)
        return reply
    
    except Exception as e:
        print(f"❌ GPT fallback error: {e}")
        return "⚠️ I'm having trouble replying right now. Please try again later."

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 10000))
    print("MODEL FOLDER CONTENTS (on startup):", os.listdir("./pretrained/dialo") if os.path.exists("./pretrained/dialo") else "Model folder missing!")
    app.run(host="0.0.0.0", port=port)
