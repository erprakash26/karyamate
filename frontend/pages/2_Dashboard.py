import streamlit as st
import requests

st.title("📋 Task Dashboard")

st.write("Welcome to your dashboard! Here you will manage tasks.")

# Placeholder: Add task button
if st.button("➕ New Task"):
    st.info("Task creation will be implemented in Module 3+ with API integration.")

# Placeholder: Task list
st.subheader("Your Tasks")
st.table(
    [
        {"ID": 1, "Title": "Buy groceries", "Completed": False},
        {"ID": 2, "Title": "Finish Module 2 report", "Completed": True},
    ]
)
