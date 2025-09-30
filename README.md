<p align="center">
  <img src="frontend/assets/logo.png" alt="KaryaMate Logo" width="200"/>
</p>

# KaryaMate — Modern Task Manager Web Application

## 📌 Overview
**KaryaMate** is a modern task manager web application designed to help you stay productive, organized, and focused.  
The name comes from the Sanskrit word **“Karya”** (task/work) combined with **“Mate”**, symbolizing a companion.  
Together, it reflects the app’s purpose: **your smart companion for tasks**.

---

## ⚡ Features
- 🔑 User registration & login (JWT authentication)  
- 📝 Create, update, and delete tasks  
- ✅ Mark tasks as completed or pending  
- 🔍 Search and filter tasks  
- 📊 Planned extensions: due dates, priority levels, CSV import, API integrations  
- ☁️ Deployment-ready: Render/Heroku for backend, Streamlit Cloud for frontend  

---

## 🏗️ Tech Stack
- **Backend**: Flask (REST API, CRUD, JWT authentication)  
- **Database**: SQLite (development) → PostgreSQL (deployment)  
- **Frontend**: Streamlit (interactive UI)  
- **Docs**: Swagger/OpenAPI (API documentation)  
- **Testing**: Postman  
- **Version Control**: Git + GitHub  
- **Deployment**: Render/Heroku (backend), Streamlit Cloud (frontend)  

---

## 📂 Project Structure
```text
karyamate/
├─ backend/                # Flask backend (API, DB, Auth)
│  ├─ app.py               # Main Flask app
│  ├─ routes.py            # API routes
│  ├─ models.py            # Database models
│  ├─ config.py            # Configurations
│  └─ requirements.txt     # Backend dependencies
│
├─ frontend/               # Streamlit frontend
│  ├─ frontend.py          # Main UI file
│  └─ assets/              # Logo + favicon
│
├─ docs/                   # Documentation
│  ├─ mockups/             # Wireframes
│  └─ api/                 # OpenAPI specification
│
├─ .gitignore
├─ README.md
└─ requirements.txt        # Global dependencies




karyamate/
├── backend/
│   ├── instance/
│   │   └── db.sqlite3
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── auth.py
│   │   └── tasks.py
│   ├── app.py
│   ├── config.py
│   ├── extensions.py
│   ├── models.py
│   ├── utils.py
│   ├── routes.py
│   ├── Procfile
│   ├── render.yaml
│   ├── requirements.txt
│   └── runtime.txt
│
├── docs/
│   ├── api/
│   │   └── openapi.yaml
│   └── mockups/
│       └── Wireframes.md
│
├── frontend/
│   ├── assets/
│   │   ├── favicon.ico
│   │   └── logo.png
│   ├── pages/
│   │   ├── 1_Login.py
│   │   └── 2_Dashboard.py
│   ├── frontend.py
│   └── home.py
│
├── .gitignore
├── LICENSE
├── README.md
├── requirements.txt
└── run_backend.bat

---

### 🚀 Getting Started

### 1. Clone the Repository
```bash
git clone https://github.com/<your-username>/karyamate.git
cd karyamate
```

### 2. Create Virtual Environment
```bash
python -m venv .venv
.venv\Scripts\activate   # Windows
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

---

## 🖥️ Running the Application

### Start Backend (Flask API)
```bash
cd backend
flask run
```
➡ Visit [http://127.0.0.1:5000/health](http://127.0.0.1:5000/health)  
Expected response:
```json
{"status": "ok"}
```

### Start Frontend (Streamlit UI)
Open a new terminal:
```bash
cd frontend
streamlit run frontend.py
```
➡ A browser window will open showing **KaryaMate** with your logo and a *Check Backend Status* button.

---

## 🧪 Testing
- Use **Postman** to test API endpoints (`/auth/register`, `/auth/login`, `/tasks`).  
- Check `docs/api/openapi.yaml` for API contract and schema.  
- Extend with Swagger UI integration later.  

---

## 📜 Roadmap
- ✅ Basic project setup  
- ✅ Backend health check  
- ✅ Frontend integration with backend  
- 🔜 User authentication & task CRUD  
- 🔜 API documentation (Swagger/OpenAPI)  
- 🔜 Deployment (Render/Heroku + Streamlit Cloud)  

---

✨ **KaryaMate — Your Smart Companion for Tasks**
=======
✅ Frontend integration with backend

🔜 User authentication & task CRUD

🔜 API documentation (Swagger/OpenAPI)

🔜 Deployment (Render/Heroku + Streamlit Cloud)



✨ KaryaMate — Your Smart Companion for Tasks.

