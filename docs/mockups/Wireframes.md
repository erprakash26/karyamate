# KaryaMate Wireframes

## 1. Login / Register Page
+-----------------------------------------------------------+
| [Logo: KaryaMate] |
| |
| [Tab: Login] [Tab: Register] |
| |
| Email: [] |
| Password: [] |
| |
| [Login Button] |
| [Switch to Register link] |
+-----------------------------------------------------------+


**Notes**:
- User can toggle between Login and Register.
- JWT token will be stored after login.

---

## 2. Task Dashboard
+--------------------------------------------------------------------------------+
| Header: KaryaMate (Logo + App Title) |
| [User Email Display] [Logout Button] |
+--------------------------------------------------------------------------------+
| Sidebar Filters |
| - Search [] |
| - Status: [All | Open | Completed] |
| |
| Main Content |
| [ + New Task Button ] |
| |
| Task List: |
| - [ ] Task Title [Edit] [Delete] Due: -- Priority: -- |
| - [✓] Completed Task [Edit] [Delete] Due: -- Priority: -- |
| |
| Modal: Create/Edit Task |
| - Title [_____________] |
| - Description [___] |
| - Completed [ ] |
| - Save / Cancel buttons |
+--------------------------------------------------------------------------------+


**Notes**:
- Basic fields: `title`, `description`, `completed`.  
- Extensions (later): `due_date`, `priority`, CSV import.  