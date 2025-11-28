import streamlit as st
import requests
from pathlib import Path

# ------------------- Page Config -------------------
THIS_DIR = Path(__file__).parent
FAVICON_PATH = THIS_DIR / "assets" / "favicon.ico"
LOGO_PATH = THIS_DIR / "assets" / "logo.png"

st.set_page_config(
    page_title="KaryaMate - Task Manager",
    page_icon=str(FAVICON_PATH),
    layout="wide",
)

# ------------------- Backend Config -------------------
API_BASE_URL = "https://karyamate-api.onrender.com"
if "API_BASE_URL" not in st.session_state:
    st.session_state["API_BASE_URL"] = API_BASE_URL

# ------------------- Custom CSS -------------------
st.markdown(
    """
    <style>
    body {
        background-color: #f5f7fb;
    }
    .main {
        background-color: #ffffff;
    }

    /* Make the main content start below the fixed nav bar */
    .block-container {
        padding-top: 2.5rem !important;  /* adjust if header height changes */
    }

    /* FIXED top nav with logo + buttons */
    .nav-fixed-wrapper {
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        z-index: 1000;
        background: rgba(255,255,255,0.97);
        backdrop-filter: blur(12px);
        border-bottom: 1px solid #e3e6f2;
        padding-top: 0.25rem;
        padding-bottom: 0.25rem;
    }

    .hero {
        background: linear-gradient(120deg, #4e8cff, #6dd5fa);
        color: white;
        padding: 2.1rem 2.4rem;
        border-radius: 18px;
        margin-top: 10px;
        margin-bottom: 25px;
        box-shadow: 0 14px 30px rgba(15,23,42,0.20);
    }
    .hero-title {
        font-size: 2.3rem;
        font-weight: 750;
        margin-bottom: 0.4rem;
    }
    .hero-subtitle {
        font-size: 1.05rem;
        opacity: 0.96;
        line-height: 1.6;
        max-width: 52rem;
    }

    .feature-card {
        background-color: #f3f5fb;
        padding: 1.2rem;
        border-radius: 12px;
        height: 100%;
        border: 1px solid #e1e5f2;
    }
    .how-card {
        background-color: #ffffff;
        padding: 1.2rem;
        border-radius: 12px;
        border: 1px dashed #d3d8eb;
    }
    .tagline {
        background-color: #eef3ff;
        padding: 16px;
        border-radius: 12px;
        text-align: center;
        font-style: italic;
        color: #333;
        margin-top: 30px;
    }
    .api-box {
        border: 3px solid #ff4d4f;
        border-radius: 12px;
        padding: 1rem;
        margin-top: 0.75rem;
        margin-bottom: 0.5rem;
        background-color: #fffefe;
        box-shadow: 0 6px 18px rgba(15,23,42,0.08);
    }
    footer {
        text-align: center;
        margin-top: 40px;
        color: gray;
        font-size: 0.85rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# =====================================================
# FIXED TOP BAR: Logo + Nav buttons
# =====================================================
st.markdown('<div class="nav-fixed-wrapper">', unsafe_allow_html=True)

nav_logo_col, nav_spacer, nav_btn_col = st.columns([1.2, 2.5, 2])

with nav_logo_col:
    # Bigger logo on the left
    st.image(str(LOGO_PATH), width=280)

with nav_btn_col:
    c1, c2, c3 = st.columns(3)
    with c1:
        if st.button("🔑 Login", use_container_width=True):
            st.switch_page("pages/1_login.py")
    with c2:
        if st.button("📋 Dashboard", use_container_width=True):
            st.switch_page("pages/2_dashboard.py")
    with c3:
        st.link_button(
            "📘 API Docs",
            f"{API_BASE_URL}/docs/",
            use_container_width=True,
        )

st.markdown("</div>", unsafe_allow_html=True)

# =====================================================
# HERO SECTION (text only, under the fixed header)
# =====================================================
st.markdown(
    """
    <div class="hero">
        <div class="hero-title">KaryaMate — Your Smart Companion for Tasks</div>
        <div class="hero-subtitle">
            Stay <b>organized, productive, and on track</b> with a modern task manager.
            Built with Flask, PostgreSQL, and Streamlit — and powered by a live REST API.
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# Optional big CTA buttons below hero
cta_col1, cta_col2 = st.columns(2)
with cta_col1:
    if st.button("🔑 Go to Login Page", use_container_width=True, key="hero_login"):
        st.switch_page("pages/1_login.py")

with cta_col2:
    if st.button("📋 View Task Dashboard", use_container_width=True, key="hero_dash"):
        st.switch_page("pages/2_dashboard.py")

st.markdown("---")

# =====================================================
# FEATURES SECTION
# =====================================================
st.subheader("✨ Why KaryaMate?")

f1, f2, f3 = st.columns(3)
with f1:
    st.markdown(
        """
        <div class="feature-card">
            <h4>🔐 Secure Authentication</h4>
            <p>Register and log in with JWT-based auth connected to a live Flask API.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

with f2:
    st.markdown(
        """
        <div class="feature-card">
            <h4>📝 Task Management</h4>
            <p>Easily create, update, complete, and delete tasks. Stay organized, structured, and always within reach.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

with f3:
    st.markdown(
        """
        <div class="feature-card">
            <h4>📊 Live API-Driven UI</h4>
            <p>Stay in control with a clean and dynamic interface that updates instantly as you manage your tasks.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

# =====================================================
# HOW IT WORKS
# =====================================================
st.subheader("⚙️ How It Works")

h1, h2, h3 = st.columns(3)
with h1:
    st.markdown(
        """
        <div class="how-card">
            <b>1. Sign Up or Log In</b><br/>
            Create your account or log in to access your personalized workspace.
        </div>
        """,
        unsafe_allow_html=True,
    )
with h2:
    st.markdown(
        """
        <div class="how-card">
            <b>2. Manage Tasks</b><br/>
            Use the dashboard to add, edit, complete, or delete tasks with our Tasks API.
        </div>
        """,
        unsafe_allow_html=True,
    )
with h3:
    st.markdown(
        """
        <div class="how-card">
            <b>3. Stay Organized</b><br/>
            Filter by status, set due dates, and keep your to-do list under control.
        </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown("---")

# =====================================================
# API-POWERED PREVIEW (Module 6 RED BOX AREA)
# =====================================================
st.subheader("🟥 API-Powered Task Preview")

st.write(
    "This area is driven by live API data from:\n\n"
    "**GET `/api/tasks`** (Authorization: Bearer `<JWT>`)."
)

## st.markdown('<div class="api-box">', unsafe_allow_html=True)

preview_tasks = []
error_msg = None

if "access_token" in st.session_state and st.session_state.access_token:
    token = st.session_state.access_token
    headers = {"Authorization": f"Bearer {token}"}

    try:
        with st.spinner("Calling GET /api/tasks ..."):
            resp = requests.get(
                f"{API_BASE_URL}/api/tasks",
                headers=headers,
                timeout=10,
            )
        if resp.status_code == 200:
            preview_tasks = resp.json()
        else:
            try:
                msg = resp.json().get("message", resp.text)
            except Exception:
                msg = resp.text
            error_msg = f"API returned {resp.status_code}: {msg}"
    except Exception as e:
        error_msg = f"Error contacting API: {e}"
else:
    st.info("Login first (Login Page) to preview your tasks here.")

if preview_tasks:
    st.success(
        f"Loaded {len(preview_tasks)} task(s) from GET /api/tasks for this user."
    )
    st.session_state["preview_tasks"] = preview_tasks

    rows = []
    for t in preview_tasks[:3]:
        rows.append(
            {
                "Title": t.get("title"),
                "Priority": t.get("priority"),
                "Completed": bool(t.get("completed")),
                "Due": (t.get("due_date") or "")[:10],
            }
        )
    st.table(rows)

elif error_msg:
    st.error(error_msg)

st.markdown("</div>", unsafe_allow_html=True)

st.caption(
    "🟥 This red box uses **GET `/api/tasks`** (method: **GET**). "
    "The response is stored in `st.session_state['preview_tasks']` "
    "and rendered as a small preview table."
)

# =====================================================
# TAGLINE + FOOTER
# =====================================================
st.markdown(
    """
    <div class="tagline">
        💡 “Organize today, achieve tomorrow — with <b>KaryaMate</b>.”
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <footer>
        © 2025 KaryaMate — Built with Flask, PostgreSQL, JWT, and Streamlit.
    </footer>
    """,
    unsafe_allow_html=True,
)
