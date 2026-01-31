<p align="center">
  <img src="frontend/assets/logo.png" alt="KaryaMate Logo" width="200"/>
</p>

# KaryaMate — Modern Task Manager Web Application

## 📌 Overview
**KaryaMate** is a modern task manager web-application designed to help you stay productive, organized, and focused.  
The name comes from the Nepali/Sanskrit word **“Karya”** (task/work) combined with **“Mate”**, symbolizing a companion.  
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
├─ backend/                     # Flask backend (API, DB, Auth, Config)
│  ├─ app.py                    # Main Flask application entry point
│  ├─ routes.py                 # Central route handler
│  ├─ routes/                   # Modular route files
│  │   ├─ __init__.py           # Package initializer
│  │   ├─ auth.py               # Authentication routes
│  │   └─ tasks.py              # Task-related routes
│  ├─ models.py                 # Database models
│  ├─ config.py                 # App configuration (env, DB URI, etc.)
│  ├─ extensions.py             # Flask extensions (db, login, etc.)
│  ├─ utils.py                  # Helper/utility functions
│  ├─ instance/                 # Local instance (ignored in Git usually)
│  │   └─ db.sqlite3            # SQLite database file
│  ├─ requirements.txt          # Backend dependencies
│  ├─ Procfile                  # Deployment process file
│  ├─ render.yaml               # Render deployment config
│  └─ runtime.txt               # Runtime version info
│
├─ frontend/                    # Streamlit frontend
│  ├─ home.py                   # Homepage UI (Main Streamlit app)
│  ├─ pages/                    # Streamlit multi-page setup
│  │   ├─ 1_login.py            # Login/Register page
│  │   └─ 2_dashboard.py        # Dashboard page
│  ├─ assets/                   # Static assets
│  │   ├─ favicon.ico           # App favicon
│  │   └─ logo.png              # App logo
│  ├─ requirements              # frontend dependencies
├─ docs/                        # Documentation part
│  ├─ api/                      # API specifications
│  │   └─ openapi.yaml          # OpenAPI schema
│  └─ mockups/                  # Design docs
│      └─ Wireframes.md         # Wireframes and UI mockups
│
├─ .gitignore                   # Git ignore rules
├─ LICENSE                      # Project license
├─ README.md                    # Project documentation
├─ requirements.txt             # Global dependencies (frontend/backend)
└─ run_backend.bat              # Helper script to run backend on Windows


---

```
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
#option 2 
```bash
cd karyamate
python -m backend.app
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

🔜 Deployment (Render/Heroku + Streamlit Cloud) (compatible with other cloud platforms).



✨ KaryaMate — Your Smart Companion for Tasks.

