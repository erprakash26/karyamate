# frontend/pages/2_dashboard.py

import streamlit as st
import requests
from datetime import datetime, date
from pathlib import Path

# ==================== Page Config ====================
THIS_DIR = Path(__file__).parent.parent  # /frontend
FAVICON_PATH = THIS_DIR / "assets" / "favicon.ico"
LOGO_PATH = THIS_DIR / "assets" / "logo.png"

st.set_page_config(
    page_title="KaryaMate - Dashboard",
    page_icon=str(FAVICON_PATH),
    layout="wide",
)

# ==================== Backend Config ====================
API_BASE_URL = st.session_state.get(
    "API_BASE_URL",
    "https://karyamate-api.onrender.com",  # deployed backend
)

# ==================== Auth Guard ====================
if "access_token" not in st.session_state or not st.session_state.access_token:
    st.title("📋 KaryaMate Task Dashboard")
    st.write("View and manage your tasks powered by the live KaryaMate API.")
    st.warning(
        "You must be logged in to view your tasks. "
        "Use the **Login** page from the sidebar."
    )
    st.stop()

TOKEN = st.session_state.access_token
HEADERS = {"Authorization": f"Bearer {TOKEN}"}

# ---- Session defaults ----
if "tasks" not in st.session_state:
    st.session_state.tasks = []          # always "all" tasks from API
if "selected_task_id" not in st.session_state:
    st.session_state.selected_task_id = None
if "show_view_dialog" not in st.session_state:
    st.session_state.show_view_dialog = False
if "view_task_data" not in st.session_state:
    st.session_state.view_task_data = None
if "show_edit_dialog" not in st.session_state:
    st.session_state.show_edit_dialog = False
if "edit_task_data" not in st.session_state:
    st.session_state.edit_task_data = None


# ==================== Helper Functions ====================
def fetch_tasks():
    """GET /api/tasks (all) and store in session_state.tasks."""
    try:
        resp = requests.get(
            f"{API_BASE_URL}/api/tasks",
            headers=HEADERS,
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
    """POST /api/tasks"""
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
        st.success("Task created successfully 🎉")
        fetch_tasks()  # refresh ALL tasks
    else:
        try:
            msg = resp.json().get("message", resp.text)
        except Exception:
            msg = resp.text
        st.error(f"❌ Could not create task ({resp.status_code}): {msg}")


def update_task(task_id, **fields):
    """PUT /api/tasks/<id> with only changed fields."""
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
    """DELETE /api/tasks/<id>."""
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


def format_priority(priority: str) -> str:
    p = (priority or "Medium").lower()
    if p == "high":
        return "🔴 High"
    if p == "low":
        return "🔵 Low"
    return "🟡 Medium"


def format_status(completed: bool) -> str:
    return "✅ Completed" if completed else "⏳ Pending"


def due_flag(due_date_str: str | None, completed: bool) -> str | None:
    """
    Return 'overdue', 'today', or None based on due date and completion.
    Only for NOT completed tasks.
    """
    if not due_date_str or completed:
        return None
    try:
        d = datetime.fromisoformat(due_date_str).date()
    except Exception:
        return None
    today = date.today()
    if d < today:
        return "overdue"
    if d == today:
        return "today"
    return None


# ==================== Header / Top Bar ====================
header_col_logo, header_col_title, header_col_btns = st.columns([1, 3, 2])

with header_col_logo:
    try:
        st.image(str(LOGO_PATH), width=150)
    except Exception:
        st.write(" ")

with header_col_title:
    st.title("📋 KaryaMate Task Dashboard")
    st.caption("View and manage your tasks powered by the live KaryaMate API.")

with header_col_btns:
    b1, b2 = st.columns(2)
    with b1:
        go_home = st.button("🏠 Home", use_container_width=True)
    with b2:
        do_logout = st.button("🚪 Logout", use_container_width=True)

    if go_home:
        st.switch_page("home.py")

    if do_logout:
        st.session_state.clear()
        st.success("You have been logged out.")
        st.switch_page("home.py")

st.markdown("---")

# ==================== Initial Fetch (ALL tasks) ====================
if "tasks_loaded_once" not in st.session_state:
    with st.spinner("Loading your tasks from the API..."):
        fetch_tasks()
    st.session_state.tasks_loaded_once = True

tasks_all = st.session_state.tasks

# ---- Overdue / today counts for metrics + focus card ----
overdue_count = 0
due_today_count = 0
for _t in tasks_all:
    flag = due_flag(_t.get("due_date"), bool(_t.get("completed")))
    if flag == "overdue":
        overdue_count += 1
    elif flag == "today":
        due_today_count += 1

# ==================== Metrics Row (always based on ALL tasks) ====================
open_count = sum(1 for t in tasks_all if not t.get("completed"))
completed_count = sum(1 for t in tasks_all if t.get("completed"))
total_count = len(tasks_all)

m1, m2, m3, m4 = st.columns(4)
m1.metric("Total Tasks", total_count)
m2.metric("Open Tasks", open_count)
m3.metric("Completed Tasks", completed_count)
m4.metric("Overdue Tasks", overdue_count)

# ---- Today's focus card ----
st.info(
    f"🗓️ Today's focus: {due_today_count} task(s) due today and {overdue_count} overdue."
)

st.markdown("---")

# ==================== Layout: Left = New Task, Right = List ====================
col_left, col_right = st.columns([1, 2])

# ---------- LEFT: Create Task ----------
with col_left:
    st.subheader("➕ New Task")

    with st.form("create_task_form", clear_on_submit=True):
        title = st.text_input("Title *")
        description = st.text_area("Description", height=80)
        priority = st.selectbox("Priority", ["Low", "Medium", "High"], index=1)
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

# ---------- RIGHT: Task List + Row Actions ----------
with col_right:
    st.subheader("🗂 Your Tasks")

    top_row1, top_row2 = st.columns([2, 2])
    with top_row1:
        status_filter = st.selectbox(
            "Filter by status",
            ["All", "Open", "Completed"],
            key="status_filter_select",
        )
    with top_row2:
        search_query = st.text_input(
            "Search (title or description)", placeholder="Type to filter tasks..."
        )

    # Refresh button (no auto-fetch on filter change)
    if st.button("🔄 Refresh"):
        with st.spinner("Refreshing tasks from API..."):
            fetch_tasks()
        tasks_all = st.session_state.tasks

    # Apply filter + search locally on tasks_all
    tasks_filtered = tasks_all
    status_val = status_filter.lower()
    if status_val == "open":
        tasks_filtered = [t for t in tasks_filtered if not t.get("completed")]
    elif status_val == "completed":
        tasks_filtered = [t for t in tasks_filtered if t.get("completed")]

    if search_query.strip():
        q = search_query.strip().lower()
        tasks_filtered = [
            t for t in tasks_filtered
            if q in (t.get("title") or "").lower()
            or q in (t.get("description") or "").lower()
        ]

    if not tasks_filtered:
        st.info("No tasks match your current filter/search. Try changing filters or create a new task.")
    else:
        # 🔴 RED BOX AREA – API-driven UI
        st.markdown("#### 📄 Task List")

        for t in tasks_filtered:
            task_id = t["id"]
            title = t.get("title", "")
            desc = t.get("description") or ""
            priority_raw = t.get("priority") or "Medium"
            completed = bool(t.get("completed"))
            due_date_str = t.get("due_date")

            with st.container(border=True):
                row1, row2 = st.columns([3, 2])

                # Row 1: title + description
                with row1:
                    st.markdown(f"**#{task_id} – {title}**")
                    if desc:
                        st.caption(desc)

                # Row 2: priority / due / status + overdue/today badge
                with row2:
                    st.markdown(f"**Priority:** {format_priority(priority_raw)}")
                    if due_date_str:
                        st.markdown(f"**Due:** {due_date_str[:10]}")
                    st.markdown(f"**Status:** {format_status(completed)}")
                    flag = due_flag(due_date_str, completed)
                    if flag == "overdue":
                        st.markdown("🔥 **Overdue**")
                    elif flag == "today":
                        st.markdown("📅 **Due today**")

                # Row 3: action buttons in one row
                a1, a2, a3, a4 = st.columns(4)
                with a1:
                    if st.button("👁 View", key=f"view_{task_id}"):
                        st.session_state.selected_task_id = task_id
                        st.session_state.view_task_data = t
                        st.session_state.show_view_dialog = True
                        st.session_state.show_edit_dialog = False
                        st.rerun()

                with a2:
                    if st.button("✏️ Edit", key=f"edit_{task_id}"):
                        st.session_state.selected_task_id = task_id
                        st.session_state.edit_task_data = t
                        st.session_state.show_edit_dialog = True
                        st.session_state.show_view_dialog = False
                        st.rerun()

                with a3:
                    if st.button("✅ Complete", key=f"complete_{task_id}") and not completed:
                        resp = update_task(task_id, completed=True)
                        if resp is not None and resp.status_code == 200:
                            st.success("Task marked as completed 🎉")
                            fetch_tasks()
                            st.rerun()
                        elif resp is not None:
                            st.error(
                                f"Failed to mark task completed ({resp.status_code}): {resp.text}"
                            )

                with a4:
                    if st.button("🗑 Delete", key=f"delete_{task_id}"):
                        resp = delete_task(task_id)
                        if resp is not None and resp.status_code in (200, 204):
                            st.success("Task deleted 🗑")
                            st.session_state.show_view_dialog = False
                            st.session_state.show_edit_dialog = False
                            st.session_state.selected_task_id = None
                            fetch_tasks()
                            st.rerun()
                        elif resp is not None:
                            st.error(
                                f"Failed to delete task ({resp.status_code}): {resp.text}"
                            )

# ==================== VIEW POPUP (MODAL) ====================
if st.session_state.show_view_dialog and st.session_state.view_task_data:

    @st.dialog("👁 Task details")
    def show_task_dialog():
        t = st.session_state.view_task_data
        st.markdown(f"### #{t['id']} – {t.get('title','')}")
        st.markdown(f"**Priority:** {format_priority(t.get('priority'))}")
        if t.get("due_date"):
            st.markdown(f"**Due:** {t['due_date'][:10]}")
        st.markdown(f"**Status:** {format_status(bool(t.get('completed')))}")
        flag = due_flag(t.get("due_date"), bool(t.get("completed")))
        if flag == "overdue":
            st.markdown("🔥 **Overdue**")
        elif flag == "today":
            st.markdown("📅 **Due today**")

        if t.get("description"):
            st.markdown("---")
            st.markdown("**Description**")
            st.write(t.get("description"))

        st.markdown("---")
        col_v1, col_v2 = st.columns(2)
        with col_v1:
            if st.button("✏️ Edit this task", use_container_width=True, key="view_to_edit"):
                st.session_state.edit_task_data = t
                st.session_state.show_edit_dialog = True
                st.session_state.show_view_dialog = False
                st.rerun()
        with col_v2:
            if st.button("Close", use_container_width=True, key="close_view_dialog"):
                st.session_state.show_view_dialog = False
                st.rerun()

    show_task_dialog()

# ==================== EDIT POPUP (MODAL) ====================
if st.session_state.show_edit_dialog and st.session_state.edit_task_data:

    @st.dialog("✏️ Edit task")
    def edit_task_dialog():
        t = st.session_state.edit_task_data

        edit_title = st.text_input(
            "Title",
            value=t.get("title", ""),
            key="dlg_edit_title",
        )
        edit_description = st.text_area(
            "Description",
            value=t.get("description") or "",
            key="dlg_edit_desc",
        )

        current_priority = (t.get("priority") or "Medium").title()
        edit_priority = st.selectbox(
            "Priority",
            ["Low", "Medium", "High"],
            index=["Low", "Medium", "High"].index(current_priority),
            key="dlg_edit_priority",
        )

        existing_due = None
        if t.get("due_date"):
            try:
                existing_due = datetime.fromisoformat(t["due_date"]).date()
            except Exception:
                existing_due = None
        edit_due = st.date_input(
            "Due date",
            value=existing_due,
            format="YYYY-MM-DD",
            key="dlg_edit_due",
        )

        edit_completed = st.checkbox(
            "Completed",
            value=bool(t.get("completed")),
            key="dlg_edit_completed",
        )

        col_e1, col_e2 = st.columns(2)
        with col_e1:
            if st.button("💾 Save changes", use_container_width=True, key="dlg_save"):
                resp = update_task(
                    t["id"],
                    title=edit_title.strip(),
                    description=edit_description.strip(),
                    priority=edit_priority,
                    completed=edit_completed,
                    due_date=edit_due,
                )
                if resp is not None and resp.status_code == 200:
                    st.success("Task updated successfully ✅")
                    st.session_state.show_edit_dialog = False
                    fetch_tasks()
                    st.rerun()
                elif resp is not None:
                    st.error(
                        f"Failed to update task ({resp.status_code}): {resp.text}"
                    )

        with col_e2:
            if st.button("Cancel", use_container_width=True, key="dlg_cancel"):
                st.session_state.show_edit_dialog = False
                st.rerun()

    edit_task_dialog()

# ==================== Footer (same as home) ====================
st.markdown("---")
st.caption(
    f"🔌 Powered by the live KaryaMate API "
    f"(`GET/POST /api/tasks`, `PUT/DELETE /api/tasks/{{id}}`) at `{API_BASE_URL}`."
)

st.markdown(
    """
    <style>
    footer {
        position: fixed;
        bottom: 0;
        left: 0;
        width: 100%;
        padding: 10px 0;
        background: #f4f4f4;
        text-align: center;
        font-size: 14px;
        color: #555;
    }
    </style>

    <footer>
        © 2025 KaryaMate — Built with Flask, PostgreSQL, JWT, and Streamlit.
    </footer>
    """,
    unsafe_allow_html=True,
)

