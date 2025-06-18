# 🌴 SmartPalmBot: AI-Driven Oil Palm Monitoring System

SmartPalmBot is a full-stack AI-powered monitoring system for oil palm plantations, combining real-time IoT sensor data, intelligent analytics, Power BI dashboards, and a chatbot assistant. It is built with Python, Flask, Azure SQL, and integrates automation for seamless plantation data processing and visualization.

---

## 🚀 Features

- 🌡️ Real-time temperature and humidity monitoring via TP-Link Tapo sensors
- 📊 Power BI dashboard for live data visualization and anomaly detection
- 🤖 Chatbot assistant that answers plantation-related queries conversationally
- ☁️ Azure SQL integration for scalable cloud data storage
- 🔄 Automation using Azure Functions & Power Automate
- 📩 Email notifications for successful or failed data updates
- 🌱 Predictive analytics using decision tree & random forest models

---

## 🛠 Tech Stack

| Layer       | Technology                         |
|-------------|-------------------------------------|
| Backend     | Python, Flask, PyODBC, Pandas       |
| Frontend    | HTML, CSS (custom + Bootstrap), JS  |
| Visualization | Power BI                          |
| Database    | Azure SQL Server                    |
| ML Models   | Scikit-learn (Decision Tree, Random Forest) |
| Automation  | Azure Function Apps, Power Automate |
| Notifications | Gmail (SMTP Email Alerts)        |

---

## 📂 Project Structure

```
SmartPalmBot/
├── app.py                  # Flask app
├── data_processing.py      # AI analysis & prediction script
├── data_update.py          # Automated sensor data ingestion
├── requirements.txt
├── templates/
│   ├── index.html          # Front page
│   └── chat.html           # Chatbot UI
├── static/
│   ├── style.css
│   ├── chatbot-logo.png
│   └── main.js
└── .gitignore
```

---

## 🧪 Setup Instructions

### 1. Clone the repo

```bash
git clone https://github.com/dayangs/FYP_SmartPalmBot.git
cd FYP_SmartPalmBot
```

### 2. Create and activate virtual environment

```bash
python -m venv chatbot-env
.\chatbot-env\Scriptsctivate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the app

```bash
python app.py
```

Then open your browser at [http://localhost:5000](http://localhost:5000)

---

## ⚠️ Security Notice

- API keys, passwords, and database credentials are hardcoded in dev but should be moved to a `.env` file in production.
- Always exclude `chatbot-env/`, `__pycache__/`, and `.env` using `.gitignore`

---

## 📬 Contact

**Dayang Nadirah binti Mohd Annuar**  
Bachelor of Computer Science (Hons)  
Universiti Malaysia Sarawak (UNIMAS)  
📧 79189@siswa.unimas.my

---

## 📄 License

This project is developed for academic and research purposes under the UNIMAS FYP program.
