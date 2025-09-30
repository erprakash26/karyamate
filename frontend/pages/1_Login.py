import streamlit as st
import requests

st.title("🔑 Login / Register")

tab1, tab2 = st.tabs(["Login", "Register"])

with tab1:
    email = st.text_input("Email", key="login_email")
    password = st.text_input("Password", type="password", key="login_password")
    if st.button("Login"):
        st.info("➡️ Login functionality will connect to /api/auth/login in Module 3")

with tab2:
    email = st.text_input("Email", key="register_email")
    password = st.text_input("Password", type="password", key="register_password")
    if st.button("Register"):
        st.info("➡️ Register functionality will connect to /api/auth/register in Module 3")
