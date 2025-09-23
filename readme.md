<p align="center">
  <img src="frontend/assets/logo.png" alt="KaryaMate Logo" width="200"/>
</p>

# KaryaMate — Modern Task Manager Web Application

## 📌 Overview
**KaryaMate** is a modern task manager web application designed to help you stay productive, organized, and focused.  
The name comes from the Sanskrit word **“Karya”** (task/work) combined with **“Mate”**, symbolizing a companion.  
Together, it reflects the app’s purpose: **your smart companion for tasks**.

---

## ⚡ Tech Stack
- **Backend**: Flask (REST API, CRUD, JWT authentication)  
- **Database**: SQLite (development) → PostgreSQL (deployment)  
- **Frontend**: Streamlit (interactive UI)  
- **Docs**: Swagger/OpenAPI (API documentation)  
- **Testing**: Postman  
- **Version Control**: Git + GitHub  
- **Deployment**: Render/Heroku (backend), Streamlit Cloud (frontend)  

---

## 📂 Project Structure
karyamate/
├─ backend/ → Flask backend (API, DB, Auth)
├─ frontend/ → Streamlit frontend
│ └─ assets/ → Logo + Favicon
├─ docs/ → Mockups, API spec, schema diagrams
├─ .gitignore
├─ README.md
└─ requirements.txt

2. Create Virtual Environment
python -m venv .venv
.venv\Scripts\activate   # Windows

3. Install Dependencies
pip install -r requirements.txt

4. Run Backend (Flask)
cd backend
flask run


➡ Open http://127.0.0.1:5000/health

5. Run Frontend (Streamlit)
cd frontend
streamlit run frontend.py


➡ Opens Streamlit app with your logo, favicon, and backend check button.

📜 Features (Planned)

✅ User registration & login

✅ Create, update, delete tasks

✅ Mark tasks as completed

🔜 Due dates & priorities

🔜 CSV import / external API integration

🔜 Cloud deployment (backend + frontend)

✨ KaryaMate — Your Smart Companion for Tasks.


---

# 📄 `.gitignore`

```gitignore
# Python cache
__pycache__/
*.py[cod]
*.pyo
*.pyd

# Virtual environments
.venv/
env/
venv/

# Databases
*.sqlite3
*.db

# Environment variables
.env

# VS Code settings
.vscode/

# OS/System files
.DS_Store
Thumbs.db

