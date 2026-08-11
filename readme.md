# 📊 Data Analytics Dashboard

A full-stack data analytics dashboard that ingests **JSON, CSV, and XML data**, processes and cleans it using Pandas, stores the processed data in PostgreSQL, and presents interactive business insights through a React dashboard.

## 🚀 Live Demo

**Frontend:**
https://data-analytics-dashboard-nine.vercel.app

**Backend API:**
https://data-analytics-dashboard-dci3.onrender.com

---

## ✨ Features

### Data Ingestion

- JSON data ingestion
- Nested JSON flattening
- CSV data ingestion
- XML data ingestion
- Multi-file data upload
- Test-data fallback for local development

### Data Processing

- Pandas-based dataset merging
- Data cleaning and type conversion
- Revenue calculation
- Delivery performance analysis
- Delayed order detection
- Analytics data generation

### Analytics Dashboard

- Total Revenue KPI
- Total Orders KPI
- Delayed Orders KPI
- Average Order Value KPI
- Revenue trend visualization
- Top products analysis
- Category-wise revenue analysis
- Delivery performance analysis
- Category filtering
- Status filtering
- Date range filtering
- Currency conversion

### UI

- Responsive React dashboard
- Interactive charts
- Light/Dark theme
- Clean analytics-focused interface

---

## 🛠️ Tech Stack

### Frontend

- React
- CSS
- Recharts
- Axios

### Backend

- Python
- Flask
- Pandas
- Flask-CORS

### Database

- PostgreSQL

### Deployment

- Vercel — Frontend
- Render — Backend
- Render PostgreSQL — Database

---

## 🔄 Data Flow

```text
JSON / CSV / XML
       ↓
Data Ingestion
       ↓
Parsing & Flattening
       ↓
Data Cleaning
       ↓
Pandas Processing
       ↓
PostgreSQL
       ↓
Analytics APIs
       ↓
React Dashboard
```

---

## 🗄️ Database

The application uses **PostgreSQL** for persistent data storage.

Main tables include:

- `orders`
- `products`
- `shipments`
- `analytics_data`

The database layer is separated from the application logic, allowing the backend to process uploaded datasets and generate analytics dynamically.

---

## 📁 Project Structure

```text
data-analytics-dashboard/
│
├── backend/
│   ├── data/
│   ├── routes/
│   ├── app.py
│   ├── database.py
│   ├── parser.py
│   ├── services.py
│   ├── requirements.txt
│   └── ...
│
├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── components/
│   │   ├── ...
│   │   └── App.jsx
│   ├── package.json
│   └── ...
│
└── README.md
```

---

## ⚙️ Local Setup

### 1. Clone the repository

```bash
git clone https://github.com/khushbuChaudhary2213/data-analytics-dashboard.git
cd data-analytics-dashboard
```

### 2. Backend Setup

```bash
cd backend
python -m venv venv
```

Activate the virtual environment.

**Windows:**

```bash
venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Configure the required environment variables in `.env`:

```env
DATABASE_URL=your_postgresql_connection_string
FRONTEND_URL=http://localhost:3000
BASE_CURRENCY=INR
```

Run the backend:

```bash
python app.py
```

The Flask API will run locally on:

```text
http://localhost:5000
```

### 3. Frontend Setup

Open another terminal:

```bash
cd frontend
npm install
npm start
```

The React application will run on:

```text
http://localhost:3000
```

---

## 🌐 Deployment

The application is deployed using:

```text
React Frontend → Vercel
Flask Backend → Render
PostgreSQL → Render
```

Environment variables are configured separately on the deployment platforms to keep credentials and configuration secure.

---

## 🔐 Environment Variables

### Backend

```env
REST_COUNTRIES_API_KEY=your_rest_countries_api_key
DATABASE_URL=your_postgresql_connection_string
FRONTEND_URL=your_frontend_url
BASE_CURRENCY=USD
```

### Frontend

```env
REACT_APP_API_URL=your_backend_url
```

---

## 🎯 Project Objective

The goal of this project is to build a complete data analytics pipeline that can accept datasets from multiple formats, transform and combine them into a unified structure, store the processed data, and provide meaningful business insights through an interactive dashboard.

The project demonstrates full-stack development along with practical data processing and analytics concepts.

---

## 👩‍💻 Author

**Khushbu Chaudhary**

B.Tech Computer Science Engineering

GitHub:
https://github.com/khushbuChaudhary2213/data-analytics-dashboard
