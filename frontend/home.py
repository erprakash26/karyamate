import streamlit as st
import requests
from pathlib import Path

# Get the directory where home.py is located
THIS_DIR = Path(__file__).parent

# Build the absolute paths
ASSETS_DIR = THIS_DIR / "assets"
LOGO_PATH = ASSETS_DIR / "logo.png"
FAVICON_PATH = ASSETS_DIR / "favicon.ico"

# ------------------- Config -------------------
API_BASE_URL = "https://karyamate-api.onrender.com"
# For local testing:
# API_BASE_URL = "http://127.0.0.1:5000"

# ------------------- Page Config -------------------
st.set_page_config(
    page_title="KaryaMate",
    page_icon=str(FAVICON_PATH),
    layout="wide"
)

# ------------------- Session State -------------------
if "page" not in st.session_state:
    st.session_state.page = "home"

# JWT token is expected to be set by pages/1_login.py
if "access_token" not in st.session_state:
    st.session_state.access_token = None

def go_to(page: str):
    st.session_state.page = page
    st.rerun()

# ------------------- Custom CSS -------------------
st.markdown(
    """
    <style>
    body {
        background-color: #f9f9fb;
    }
    .main {
        background-color: white;
        padding: 2rem;
        border-radius: 12px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
    }
    h1, h2, h3 {
        font-family: "Segoe UI", sans-serif;
    }
    .feature-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 10px;
        height: 100%;
    }
    .hero {
        background: linear-gradient(120deg, #4e8cff, #6dd5fa);
        color: white;
        padding: 2rem;
        border-radius: 12px;
        margin-bottom: 20px;
    }
    .tagline {
        background-color: #eef3fb;
        padding: 20px;
        border-radius: 12px;
        margin-top: 20px;
        text-align: center;
        font-style: italic;
        color: #333;
    }
    footer {
        text-align: center;
        margin-top: 40px;
        color: gray;
        font-size: 0.9rem;
    }
    .api-box {
        border: 2px solid red;
        padding: 1rem;
        border-radius: 10px;
        margin-top: 1rem;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ------------------- Hero Section -------------------
col1, col2 = st.columns([1, 5])
with col1:
    st.image(str(LOGO_PATH), width=400)
with col2:
    st.markdown(
        """
        <h3 style="margin-top:0; color:gray;">Your Smart Companion for Tasks</h3>
        """,
        unsafe_allow_html=True
    )

st.markdown("---")

# ------------------- Welcome Section -------------------
st.markdown(
    """
    <div class="hero">
        <h2>🚀 Welcome to KaryaMate</h2>
        <p>Stay <b>productive, organized, and focused</b> with a modern task manager.  
        Built with Python, Flask, and Streamlit for simplicity and speed.</p>
    </div>
    """,
    unsafe_allow_html=True
)

# ------------------- Features -------------------
st.subheader("✨ Features at a Glance")

colA, colB, colC = st.columns(3)

with colA:
    st.markdown(
        """
        <div class="feature-card">
            <h4>🔑 Authentication</h4>
            <p>Secure register and login with JWT tokens.</p>
        </div>
        """,
        unsafe_allow_html=True
    )
with colB:
    st.markdown(
        """
        <div class="feature-card">
            <h4>📝 Task Management</h4>
            <p>Create, edit, delete, and track your tasks easily.</p>
        </div>
        """,
        unsafe_allow_html=True
    )
with colC:
    st.markdown(
        """
        <div class="feature-card">
            <h4>✅ Productivity</h4>
            <p>Mark tasks as complete, filter by status, and stay organized.</p>
        </div>
        """,
        unsafe_allow_html=True
    )

st.markdown("---")

# ------------------- Demo Section -------------------
st.subheader("🔍 Quick Demo")

if st.button("Check Backend Status", use_container_width=True):
    try:
        response = requests.get(f"{API_BASE_URL}/health", timeout=10)
        if response.status_code == 200:
            st.success("✅ Backend is running")
        else:
            st.error(f"❌ Backend returned {response.status_code}")
    except Exception as e:
        st.error(f"Cannot connect to backend: {e}")

colX, colY = st.columns(2)
with colX:
    st.button("🔑 Go to Login Page", use_container_width=True, on_click=lambda: go_to("login"))
with colY:
    st.button("📋 View Task Dashboard", use_container_width=True, on_click=lambda: go_to("dashboard"))

# ------------------- API-Driven Preview (RED BOX AREA) -------------------
st.subheader("🟥 API-Powered Task Preview")

st.markdown(
    """
    This area is driven by live API data from:
    <br><b>GET /api/tasks</b> (Authorization: Bearer &lt;JWT&gt;)  
    """,
    unsafe_allow_html=True,
)

with st.container():
    st.markdown('<div class="api-box">', unsafe_allow_html=True)

    token = st.session_state.access_token

    if not token:
        st.info("Login first (🔑 Login Page) to preview your tasks here.")
    else:
        headers = {"Authorization": f"Bearer {token}"}
        try:
            with st.spinner("Loading tasks from API..."):
                resp = requests.get(f"{API_BASE_URL}/api/tasks", headers=headers, timeout=10)

            if resp.status_code == 200:
                tasks = resp.json()
                if tasks:
                    st.write("Tasks loaded from API:")

                    # Simple table view
                    for t in tasks:
                        st.markdown(
                            f"""
                            **{t.get('title', '(no title)')}**  
                            • Description: {t.get('description') or '-'}  
                            • Completed: {'✅' if t.get('completed') else '❌'}  
                            • Priority: {t.get('priority') or '-'}  
                            """
                        )
                        st.markdown("---")
                else:
                    st.warning("No tasks found. Try creating one from the Dashboard.")
            else:
                st.error(f"Failed to load tasks. Status code: {resp.status_code}")
                st.text(resp.text)
        except Exception as e:
            st.error(f"Error while calling /api/tasks: {e}")

    st.markdown('</div>', unsafe_allow_html=True)

# ------------------- Tagline -------------------
st.markdown(
    """
    <div class="tagline">
        💡 “Organize today, achieve tomorrow — with KaryaMate.”
    </div>
    """,
    unsafe_allow_html=True
)

# ------------------- Footer -------------------
st.markdown(
    """
    <footer>
    © 2025 KaryaMate
    </footer>
    """,
    unsafe_allow_html=True
)

# ------------------- Page Routing -------------------
if st.session_state.page == "login":
    st.switch_page("pages/1_login.py")
elif st.session_state.page == "dashboard":
    st.switch_page("pages/2_dashboard.py")
