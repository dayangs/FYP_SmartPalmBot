# 🌴 SmartPalmBot: AI-Driven Oil Palm Monitoring System

SmartPalmBot is a full-stack AI-powered monitoring system for oil palm plantations, combining real-time IoT sensor data, intelligent analytics, Power BI dashboards, and a chatbot assistant. It is built with Python, Flask, Azure SQL, and integrates automation for seamless plantation data processing and visualization.

---

## 🚀 Features

- 🌡️ Real-time temperature and humidity monitoring via TP-Link Tapo sensors
- 📊 Power BI dashboard for live data visualization and anomaly detection
- 🤖 Chatbot assistant that answers plantation-related queries conversationally (sensor data only on cloud, AI fallback locally)
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
├── download_model.py       # (For local AI fallback only)
├── data_processing.py      # AI analysis & prediction script
├── requirements.txt
├── templates/
│   ├── index.html          # Front page (with Power BI)
│   └── chat.html           # Chatbot UI
├── static/
│   ├── style.css
│   ├── favicon.png
│   ├── palm-oil-background.jpg
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

### 4. (Optional, for AI chatbot) Download DialoGPT model
Skip this on cloud deployment—local only!
```bash
python download_model.py
```

### Run the app
```bash
python app.py
```

Then open your browser at http://localhost:10000 or your configured port.
---

## ⚠️ Deployment & Limitations

Cloud Deployment (Render, etc.):

- Database integration, sensor query, and Power BI dashboard features are available online.

- AI chatbot fallback (DialoGPT) is disabled on free cloud hosts due to RAM limits; users will receive a message indicating the AI is offline.

Local Deployment:

- All features work, including AI chatbot fallback (DialoGPT) for general conversation.

Note:For demo/viva, the AI chatbot is shown running locally. Limitation is documented in system report.

---

## ⚠️ Security Notice
All credentials and passwords are for development use only.Use a .env file and environment variables in production.

Do not commit sensitive data to GitHub.

## 📬 Contact
**Dayang Nadirah binti Mohd Annuar**  
Bachelor of Computer Science (Hons)  
Universiti Malaysia Sarawak (UNIMAS)  
📧 79189@siswa.unimas.my

---

## 📄 License

This project is developed for academic and research purposes under the UNIMAS FYP program.
