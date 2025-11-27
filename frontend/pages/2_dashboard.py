import streamlit as st
import requests
from datetime import datetime, date
from pathlib import Path

# ==================== Page Config ====================
THIS_DIR = Path(__file__).parent.parent  # go up from /pages to /frontend
FAVICON_PATH = THIS_DIR / "assets" / "favicon.ico"

st.set_page_config(
    page_title="KaryaMate - Dashboard",
    page_icon=str(FAVICON_PATH),
    layout="wide",
)

# ==================== Backend Config ====================
API_BASE_URL = st.session_state.get(
    "API_BASE_URL",
    "https://karyamate-api.onrender.com",  # deployed backend
# For local testing, you can temporarily use:
# API_BASE_URL = "http://127.0.0.1:5000"
)

# ==================== Auth Guard ====================
# If there is no access token, block the page completely
if "access_token" not in st.session_state or not st.session_state.access_token:
    st.title("📋 KaryaMate Task Dashboard")
    st.write("View and manage your tasks powered by the live KaryaMate API.")
    st.warning(
        "You must be logged in to view your tasks. "
        "Go back to the **Login** page from the side menu."
    )
    st.stop()

# We *do* have a token → from here on we are logged in
TOKEN = st.session_state.access_token
HEADERS = {"Authorization": f"Bearer {TOKEN}"}

# Ensure tasks list exists in session
if "tasks" not in st.session_state:
    st.session_state.tasks = []


# ==================== Helper Functions ====================
def fetch_tasks(status: str = "all"):
    """
    Call GET /api/tasks with optional ?status=open|completed|all
    and store result into st.session_state.tasks.
    """
    try:
        params = {}
        if status in ("open", "completed"):
            params["status"] = status

        resp = requests.get(
            f"{API_BASE_URL}/api/tasks",
            headers=HEADERS,
            params=params,
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
    elif resp.status_code == 401:
        st.error("Unauthorized (401). Your session may have expired. Please log in again.")
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
        payload["due_date"] = datetime.combine(
            due_date, datetime.min.time()
        ).isoformat()

    try:
        resp = requests.post(
            f"{API_BASE_URL}/api/tasks",
            headers=HEADERS,
            json=payload,
            timeout=10,
        )
    except Exception as e:
        st.error(f"❌ Failed to create task: {e}")
        return

    if resp.status_code == 201:
        st.success("✅ Task created successfully!")
        fetch_tasks()  # refresh
    else:
        try:
            msg = resp.json().get("message", resp.text)
        except Exception:
            msg = resp.text
        st.error(f"❌ Could not create task ({resp.status_code}): {msg}")


def update_task(task_id, **fields):
    """Call PUT /api/tasks/<id> with only the changed fields."""
    payload = {}
    for key, value in fields.items():
        if value is not None:
            if key == "due_date" and isinstance(value, date):
                payload[key] = datetime.combine(value, datetime.min.time()).isoformat()
            else:
                payload[key] = value

    try:
        resp = requests.put(
            f"{API_BASE_URL}/api/tasks/{task_id}",
            headers=HEADERS,
            json=payload,
            timeout=10,
        )
    except Exception as e:
        st.error(f"❌ Failed to update task: {e}")
        return None

    return resp


def delete_task(task_id):
    """Call DELETE /api/tasks/<id>."""
    try:
        resp = requests.delete(
            f"{API_BASE_URL}/api/tasks/{task_id}",
            headers=HEADERS,
            timeout=10,
        )
    except Exception as e:
        st.error(f"❌ Failed to delete task: {e}")
        return None

    return resp


# ==================== Header ====================
st.title("📋 KaryaMate Task Dashboard")
st.write("View and manage your tasks powered by the live KaryaMate API.")

header_left, header_right = st.columns([3, 1])

with header_left:
    st.info("You are logged in. Manage your tasks below.")

with header_right:
    btn_col1, btn_col2 = st.columns(2)
    with btn_col1:
        home_btn = st.button("🏠 Home", use_container_width=True)
    with btn_col2:
        logout_btn = st.button("🚪 Logout", use_container_width=True)

# Handle nav buttons
if home_btn:
    st.switch_page("home.py")

if logout_btn:
    st.session_state.clear()
    st.success("You have been logged out.")
    st.switch_page("home.py")

st.markdown("---")

# ==================== Create Task Section ====================
col_left, col_right = st.columns([1, 2])

with col_left:
    st.subheader("➕ New Task")

    with st.form("create_task_form", clear_on_submit=True):
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
            due_value = due if isinstance(due, date) else None
            create_task(title.strip(), description.strip(), priority, due_value)

# ==================== Task List & Actions ====================
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

    tasks = st.session_state.tasks

    if not tasks:
        st.info("No tasks loaded yet. Click **Refresh Tasks** to fetch your tasks.")
    else:
        # Summary table
        table_rows = [
            {
                "ID": t.get("id"),
                "Title": t.get("title"),
                "Priority": t.get("priority"),
                "Completed": t.get("completed"),
                "Due Date": t.get("due_date"),
            }
            for t in tasks
        ]
        st.dataframe(table_rows, use_container_width=True, hide_index=True)

        st.markdown("### ✏️ Update Tasks(Edit/Complete/Delete")

        # Map task IDs to task objects
        task_ids = [t["id"] for t in tasks]
        task_map = {t["id"]: t for t in tasks}

        selected_id = st.selectbox(
            "Select a task to edit",
            task_ids,
            format_func=lambda i: f"#{i} – {task_map[i]['title']}",
        )
        selected_task = task_map[selected_id]

        # Pre-fill editor
        edit_title = st.text_input("Title", value=selected_task["title"])
        edit_description = st.text_area(
            "Description", value=selected_task.get("description") or ""
        )

        # Normalize priority to title-case ("Low", "Medium", "High")
        current_priority = (selected_task.get("priority") or "Medium").title()
        if current_priority not in ["Low", "Medium", "High"]:
            current_priority = "Medium"

        edit_priority = st.selectbox(
            "Priority",
            ["Low", "Medium", "High"],
            index=["Low", "Medium", "High"].index(current_priority),
        )

        existing_due = None
        if selected_task.get("due_date"):
            try:
                existing_due = datetime.fromisoformat(
                    selected_task["due_date"]
                ).date()
            except Exception:
                existing_due = None
        edit_due = st.date_input(
            "Due date", value=existing_due, format="YYYY-MM-DD"
        )

        edit_completed = st.checkbox(
            "Completed", value=bool(selected_task.get("completed"))
        )

        col_u1, col_u2, col_u3 = st.columns(3)

        with col_u1:
            if st.button("💾 Save Changes", use_container_width=True):
                resp = update_task(
                    selected_id,
                    title=edit_title.strip(),
                    description=edit_description.strip(),
                    priority=edit_priority,
                    completed=edit_completed,
                    due_date=edit_due,
                )
                if resp is not None and resp.status_code == 200:
                    st.success("Task updated successfully ✅")
                    fetch_tasks(status=status_filter.lower())
                    st.rerun()
                elif resp is not None:
                    st.error(f"Failed to update task ({resp.status_code}): {resp.text}")

        with col_u2:
            if st.button("✅ Mark Completed", use_container_width=True):
                resp = update_task(selected_id, completed=True)
                if resp is not None and resp.status_code == 200:
                    st.success("Task marked as completed 🎉")
                    fetch_tasks(status=status_filter.lower())
                    st.rerun()
                elif resp is not None:
                    st.error(
                        f"Failed to mark task completed ({resp.status_code}): {resp.text}"
                    )

        with col_u3:
            if st.button("🗑 Delete Task", use_container_width=True):
                resp = delete_task(selected_id)
                if resp is not None and resp.status_code in (200, 204):
                    st.success("Task deleted 🗑")
                    fetch_tasks(status=status_filter.lower())
                    st.rerun()
                elif resp is not None:
                    st.error(f"Failed to delete task ({resp.status_code}): {resp.text}")

st.markdown("---")
st.caption(
    f"🔌 This dashboard is driven by the live KaryaMate API "
    f"(`GET/POST /api/tasks`, `PUT/DELETE /api/tasks/{{id}}`) at `{API_BASE_URL}`."
)
