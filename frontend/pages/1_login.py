import streamlit as st
from pathlib import Path
import requests

# ----- Absolute path to favicon -----
THIS_DIR = Path(__file__).parent
FAVICON_PATH = THIS_DIR / "assets" / "favicon.ico"

# ------------------- Config -------------------
# Deployed backend
API_BASE_URL = "https://karyamate-api.onrender.com"
# For local testing, you can temporarily change to:
# API_BASE_URL = "http://127.0.0.1:5000"


st.set_page_config(
    page_title="KaryaMate - Login",
    page_icon=str(FAVICON_PATH),
    layout="wide",
)

st.title("🔑 Login / Register")

# Ensure session keys exist
if "access_token" not in st.session_state:
    st.session_state.access_token = None

if "page" not in st.session_state:
    st.session_state.page = "home"


def do_login(email: str, password: str):
    """Call POST /api/auth/login and store JWT on success."""
    if not email or not password:
        st.warning("Please enter both email and password.")
        return

    try:
        resp = requests.post(
            f"{API_BASE_URL}/api/auth/login",
            json={"email": email, "password": password},
            timeout=10,
        )
    except Exception as e:
        st.error(f"Could not connect to backend: {e}")
        return

    if resp.status_code == 200:
        data = resp.json()
        token = data.get("access_token")
        if not token:
            st.error("Login succeeded but no token returned.")
            return

        st.session_state.access_token = token
        st.session_state.page = "dashboard"   # tell home.py where to go
        st.success("✅ Logged in successfully!")

        # Redirect back to home, which will then route to dashboard
        try:
            st.switch_page("home.py")
        except Exception:
            # Fallback: rerun if switch_page not available
            st.rerun()
    else:
        try:
            msg = resp.json().get("message", resp.text)
        except Exception:
            msg = resp.text
        st.error(f"Login failed ({resp.status_code}): {msg}")


def do_register(email: str, password: str):
    """Call POST /api/auth/register."""
    if not email or not password:
        st.warning("Please enter both email and password.")
        return

    try:
        resp = requests.post(
            f"{API_BASE_URL}/api/auth/register",
            json={"email": email, "password": password},
            timeout=10,
        )
    except Exception as e:
        st.error(f"Could not connect to backend: {e}")
        return

    if resp.status_code == 201:
        st.success("🎉 Registration successful! You can now log in.")
    else:
        try:
            msg = resp.json().get("message", resp.text)
        except Exception:
            msg = resp.text
        st.error(f"Registration failed ({resp.status_code}): {msg}")


# ------------------- UI -------------------

tab1, tab2 = st.tabs(["Login", "Register"])

with tab1:
    st.subheader("👤 Login to KaryaMate")
    login_email = st.text_input("Email", key="login_email")
    login_password = st.text_input("Password", type="password", key="login_password")

    if st.button("Login", type="primary", use_container_width=True):
        do_login(login_email.strip(), login_password)

with tab2:
    st.subheader("Create a new account")
    register_email = st.text_input("Email", key="register_email")
    register_password = st.text_input(
        "Password",
        type="password",
        key="register_password",
        help="Please use a strong password to ensure security"
    )

    if st.button("Register", use_container_width=True):
        do_register(register_email.strip(), register_password)

# Small status hint at the bottom
if st.session_state.access_token:
    st.info("You are currently logged in. You can go to the Dashboard from the home page.")
