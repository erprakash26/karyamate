import streamlit as st
import requests
from datetime import datetime, date
from pathlib import Path

# ----- Paths / favicon -----
THIS_DIR = Path(__file__).parent
FAVICON_PATH = THIS_DIR.parent / "assets" / "favicon.ico"

# ------------------- Backend Config -------------------
API_BASE_URL = st.session_state.get(
    "API_BASE_URL",
    "https://karyamate-api.onrender.com"   # fallback to deployed API
    # For local testing, you can temporarily use:
    # API_BASE_URL = "http://127.0.0.1:5000"
)

st.set_page_config(
    page_title="KaryaMate - Dashboard",
    page_icon=str(FAVICON_PATH),
    layout="wide",
)

st.title("📋 KaryaMate Task Dashboard")
st.write("View and manage your tasks powered by the live KaryaMate API.")

# ------------------- Top Navigation -------------------
nav_col1, nav_col2, nav_col3 = st.columns([6, 1, 1])

with nav_col2:
    if st.button("🏠 Home", use_container_width=True):
        st.session_state.page = "home"
        st.switch_page("../home.py")  # go back to main home

with nav_col3:
    if st.button("🚪 Logout", use_container_width=True):
        for key in ["access_token", "page"]:
            if key in st.session_state:
                del st.session_state[key]
        st.success("Logged out successfully!")
        st.switch_page("1_login.py")


# ------------------- Auth Guard -------------------
if "access_token" not in st.session_state or not st.session_state.access_token:
    st.warning(
        "You must be logged in to view your tasks. "
        "Go back to the **Login** page from the side menu."
    )
    st.stop()

TOKEN = st.session_state.access_token
HEADERS = {"Authorization": f"Bearer {TOKEN}"}

# ------------------- API Helpers -------------------
def fetch_tasks(status: str = "all"):
    """
    Call GET /api/tasks with optional ?status=open|completed|all
    """
    try:
        params = {}
        if status in ("open", "completed"):
            params["status"] = status

        res = requests.get(
            f"{API_BASE_URL}/api/tasks",
            headers=HEADERS,
            params=params,
            timeout=10,
        )
    except Exception as e:
        return None, f"❌ Error contacting API: {e}"

    if res.status_code == 200:
        try:
            return res.json(), None
        except Exception as e:
            return None, f"❌ Could not parse tasks response: {e}"
    elif res.status_code == 401:
        return None, "❌ Unauthorized (401). Please log in again."
    else:
        try:
            msg = res.json().get("message", res.text)
        except Exception:
            msg = res.text
        return None, f"❌ Could not load tasks ({res.status_code}): {msg}"


def create_task(title: str, description: str, priority: str, due_date: date | None):
    payload = {
        "title": title,
        "description": description or "",
        "completed": False,
        "priority": priority or "medium",
        "due_date": None,
    }

    if due_date:
        # backend expects ISO datetime string
        payload["due_date"] = datetime.combine(
            due_date, datetime.min.time()
        ).isoformat()

    try:
        res = requests.post(
            f"{API_BASE_URL}/api/tasks",
            headers=HEADERS,
            json=payload,
            timeout=10,
        )
    except Exception as e:
        st.error(f"❌ Failed to create task: {e}")
        return None

    return res


def update_task(task_id, title=None, description=None, priority=None, completed=None, due_date=None):
    payload = {}
    if title is not None:
        payload["title"] = title
    if description is not None:
        payload["description"] = description
    if priority is not None:
        payload["priority"] = priority
    if completed is not None:
        payload["completed"] = completed
    if due_date is not None:
        if isinstance(due_date, date):
            payload["due_date"] = datetime.combine(
                due_date, datetime.min.time()
            ).isoformat()
        else:
            payload["due_date"] = due_date

    try:
        res = requests.put(
            f"{API_BASE_URL}/api/tasks/{task_id}",
            headers=HEADERS,
            json=payload,
            timeout=10,
        )
    except Exception as e:
        st.error(f"❌ Failed to update task: {e}")
        return None

    return res


def delete_task(task_id):
    try:
        res = requests.delete(
            f"{API_BASE_URL}/api/tasks/{task_id}",
            headers=HEADERS,
            timeout=10,
        )
    except Exception as e:
        st.error(f"❌ Failed to delete task: {e}")
        return None

    return res

# ------------------- Top Bar -------------------
top_left, top_right = st.columns([2, 1])
with top_left:
    st.info("You can create, filter, edit, complete, and delete tasks here.")

with top_right:
    if st.button("🔄 Refresh tasks", use_container_width=True):
        st.session_state["force_reload"] = True

st.markdown("---")

# ------------------- Create Task Section -------------------
st.subheader("➕ New Task")

with st.form("create_task_form", clear_on_submit=True):
    c1, c2 = st.columns([3, 1])
    with c1:
        title = st.text_input("Title *", placeholder="e.g. Finish project report")
    with c2:
        priority = st.selectbox("Priority", ["low", "medium", "high"], index=1)

    description = st.text_area("Description", height=80, placeholder="Optional notes")
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
        res = create_task(title.strip(), description.strip(), priority, due_value)
        if res is not None and res.status_code == 201:
            st.success("✅ Task created successfully!")
            st.session_state["force_reload"] = True
        elif res is not None:
            try:
                msg = res.json().get("message", res.text)
            except Exception:
                msg = res.text
            st.error(f"❌ Could not create task ({res.status_code}): {msg}")

st.markdown("---")

# ------------------- Task List + Actions -------------------
st.subheader("🗂 Your Tasks")

filter_col, _ = st.columns([1, 3])
with filter_col:
    status_filter = st.selectbox("Filter by status", ["all", "open", "completed"])

# Fetch tasks each run (or when forced)
status_param = status_filter.lower()
tasks, error = fetch_tasks(status_param)
st.session_state["force_reload"] = False

if error:
    st.error(error)
elif not tasks:
    st.info("No tasks found. Create a new one above!")
else:
    # Table view – this is your RED BOX area for the report
    st.dataframe(
        [
            {
                "ID": t.get("id"),
                "Title": t.get("title"),
                "Priority": t.get("priority"),
                "Completed": t.get("completed"),
                "Due Date": t.get("due_date"),
                "Created": t.get("created_at"),
            }
            for t in tasks
        ],
        use_container_width=True,
        hide_index=True,
    )

    st.markdown("### ✏️ Edit / ✅ Complete / 🗑 Delete")

    # Map tasks by ID
    task_ids = [t["id"] for t in tasks]
    task_map = {t["id"]: t for t in tasks}

    selected_id = st.selectbox(
        "Select a task to modify",
        task_ids,
        format_func=lambda i: f"#{i} – {task_map[i]['title']}",
    )

    selected_task = task_map[selected_id]

    # Pre-fill edit form
    edit_title = st.text_input("Edit Title", value=selected_task["title"])
    edit_description = st.text_area("Edit Description", value=selected_task.get("description") or "")
    edit_priority = st.selectbox(
        "Edit Priority",
        ["low", "medium", "high"],
        index=["low", "medium", "high"].index(selected_task.get("priority", "medium")),
    )
    edit_completed = st.checkbox("Completed", value=selected_task.get("completed", False))

    # Parse due date
    existing_due = None
    if selected_task.get("due_date"):
        try:
            existing_due = datetime.fromisoformat(selected_task["due_date"]).date()
        except Exception:
            existing_due = None

    edit_due = st.date_input(
        "Edit Due Date",
        value=existing_due,
        format="YYYY-MM-DD",
    )

    col_u1, col_u2, col_u3 = st.columns(3)

    # Save changes
    with col_u1:
        if st.button("💾 Save Changes", use_container_width=True):
            res = update_task(
                selected_id,
                title=edit_title.strip(),
                description=edit_description.strip(),
                priority=edit_priority,
                completed=edit_completed,
                due_date=edit_due,
            )
            if res is not None and res.status_code == 200:
                st.success("✅ Task updated successfully")
                st.session_state["force_reload"] = True
            elif res is not None:
                st.error(f"❌ Failed to update task ({res.status_code}): {res.text}")

    # Mark completed
    with col_u2:
        if st.button("✅ Mark Completed", use_container_width=True):
            res = update_task(selected_id, completed=True)
            if res is not None and res.status_code == 200:
                st.success("🎉 Task marked as completed")
                st.session_state["force_reload"] = True
            elif res is not None:
                st.error(f"❌ Failed to mark completed ({res.status_code}): {res.text}")

    # Delete
    with col_u3:
        if st.button("🗑 Delete Task", use_container_width=True):
            res = delete_task(selected_id)
            if res is not None and res.status_code in (200, 204):
                st.success("🗑 Task deleted")
                st.session_state["force_reload"] = True
            elif res is not None:
                st.error(f"❌ Failed to delete task ({res.status_code}): {res.text}")

st.markdown("---")
st.caption(
    f"🔌 This dashboard is powered by the live KaryaMate API: "
    f"`GET /api/tasks`, `POST /api/tasks`, `PUT /api/tasks/{{id}}`, and `DELETE /api/tasks/{{id}}` "
    f"at `{API_BASE_URL}`."
)
