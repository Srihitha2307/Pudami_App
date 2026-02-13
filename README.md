# 🌍 Pudami AI: Precision Agriculture Intelligence
**Advanced Earth Monitoring & Soil Analytics Dashboard**

Pudami AI is a sophisticated agricultural intelligence platform designed to bridge the gap between traditional farming and data-driven precision agriculture. By monitoring critical soil parameters and environmental factors, Pudami AI provides actionable insights to optimize crop yield and ensure soil sustainability.

---

## 🚀 App Description
**Pudami AI** acts as a command center for the modern farmer. Built with a focus on usability and technical depth, the application monitors:
* **Soil Health:** Real-time NPK (Nitrogen, Phosphorus, Potassium) tracking and pH balance.
* **Hydration Levels:** Precise soil moisture monitoring to prevent root desiccation or waterlogging.
* **Environmental Context:** Live weather data including Sunlight (Lux), Wind Speed, and Direction.
* **Crop Intelligence:** Dynamic thresholds for Paddy, Sugarcane, Wheat, and Soybeans pulled directly from an Airtable relational database.



---

## 🛠️ The Tech Stack
* **Frontend:** HTML5, Tailwind CSS (Design), Chart.js (Visualizations)
* **Backend:** Python 3.11+, Flask (Micro-framework)
* **Database:** Airtable (Relational Cloud CMS)
* **API:** PyAirtable (RESTful Integration)

---

## ✨ Key Features
* **Live Sensor Simulation:** Toggle between "Live Sensor" and "User Input" modes to test field scenarios.
* **Database Synchronization:** Automatically pulls optimal standards from Airtable when sensor data is unavailable.
* **AI Recommendation Engine:** Generates real-time briefings on fertilizer application and irrigation needs.
* **Health Alerts:** Monitors specific tables for Pest and Disease risks tailored to the active crop.
* **Glassmorphic UI:** A premium, olive-themed interface designed for high readability in outdoor field conditions.



---

## 📂 Project Structure
```bash
PudamiApp/
├── app.py              # Backend logic, API routes, and Airtable integration
├── static/             # Assets (Images, Custom CSS)
├── templates/          
│   └── dashboard.html  # Main Analytics UI
├── requirements.txt    # List of Python dependencies
└── README.md           # Documentation
