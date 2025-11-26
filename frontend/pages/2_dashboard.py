import streamlit as st
import requests
from datetime import datetime, date
from pathlib import Path

# ----- Absolute path to favicon -----
THIS_DIR = Path(__file__).parent
FAVICON_PATH = THIS_DIR / "assets" / "favicon.ico"

# ------------------- Backend Config -------------------
API_BASE_URL = "https://karyamate-api.onrender.com"
# For local testing, you can temporarily use:
# API_BASE_URL = "http://127.0.0.1:5000"

st.set_page_config(
    page_title="KaryaMate - Dashboard",
    page_icon=str(FAVICON_PATH),
    layout="wide",
)

st.title("📋 Task Dashboard")
st.write("View and manage your tasks powered by the live KaryaMate API.")

# ------------------- Auth Guard -------------------
if "access_token" not in st.session_state or not st.session_state.access_token:
    st.warning(
        "You must be logged in to view your tasks. "
        "Go to the **Login** page from the home screen."
    )
    st.stop()

token = st.session_state.access_token
headers = {"Authorization": f"Bearer {token}"}

if "tasks" not in st.session_state:
    st.session_state.tasks = []


# ------------------- API Helpers -------------------
def fetch_tasks(status: str = "all"):
    """Call GET /api/tasks and store in session_state.tasks."""
    try:
        resp = requests.get(
            f"{API_BASE_URL}/api/tasks",
            headers=headers,
            params={"status": status},
            timeout=10,
        )
    except Exception as e:
        st.error(f"❌ Failed to fetch tasks: {e}")
        return

    if resp.status_code == 200:
        try:
            st.session_state.tasks = resp.json()
        except Exception as e:
            st.error(f"❌ Could not parse tasks response: {e}")
    else:
        try:
            msg = resp.json().get("message", resp.text)
        except Exception:
            msg = resp.text
        st.error(f"❌ Could not load tasks ({resp.status_code}): {msg}")


def create_task(title: str, description: str, priority: str, due_date: date | None):
    """Call POST /api/tasks to create a new task."""
    payload = {
        "title": title,
        "description": description or "",
        "completed": False,
        "priority": priority,
        "due_date": None,
    }

    if due_date:
        # backend expects ISO datetime string
        payload["due_date"] = datetime.combine(
            due_date, datetime.min.time()
        ).isoformat()

    try:
        resp = requests.post(
            f"{API_BASE_URL}/api/tasks",
            headers=headers,
            json=payload,
            timeout=10,
        )
    except Exception as e:
        st.error(f"❌ Failed to create task: {e}")
        return

    if resp.status_code == 201:
        st.success("✅ Task created successfully!")
        # Refresh list
        fetch_tasks()
    else:
        try:
            msg = resp.json().get("message", resp.text)
        except Exception:
            msg = resp.text
        st.error(f"❌ Could not create task ({resp.status_code}): {msg}")


# ------------------- Layout -------------------
col_left, col_right = st.columns([1, 2])

# ----- Left: Create Task -----
with col_left:
    st.subheader("➕ New Task")

    with st.form("create_task_form"):
        title = st.text_input("Title *")
        description = st.text_area("Description", height=80)
        priority = st.selectbox("Priority", ["Low", "Medium", "High"])
        due = st.date_input(
            "Due Date (optional)",
            value=None,
            format="YYYY-MM-DD",
        )

        submitted = st.form_submit_button("Create Task")

    if submitted:
        if not title.strip():
            st.warning("Title is required.")
        else:
            # date_input returns either a date or None
            due_value = due if isinstance(due, date) else None
            create_task(title.strip(), description.strip(), priority, due_value)

# ----- Right: Task List -----
with col_right:
    st.subheader("🗂 Your Tasks")

    status_filter = st.selectbox("Filter by status", ["All", "Open", "Completed"])
    if st.button("🔄 Refresh Tasks"):
        status_param = "all"
        if status_filter.lower() == "open":
            status_param = "open"
        elif status_filter.lower() == "completed":
            status_param = "completed"
        fetch_tasks(status=status_param)

    # Show current tasks
    if not st.session_state.tasks:
        st.info("No tasks loaded yet. Click **Refresh Tasks** to fetch your tasks.")
    else:
        table_rows = []
        for t in st.session_state.tasks:
            table_rows.append(
                {
                    "ID": t.get("id"),
                    "Title": t.get("title"),
                    "Priority": t.get("priority"),
                    "Completed": t.get("completed"),
                    "Due Date": t.get("due_date"),
                }
            )

        st.dataframe(table_rows, use_container_width=True)

st.markdown("---")
st.caption(
    f"🔌 This dashboard is driven by the live KaryaMate API: "
    f"`GET /api/tasks` and `POST /api/tasks` at `{API_BASE_URL}`."
)
