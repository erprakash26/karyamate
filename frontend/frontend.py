import streamlit as st
import requests

st.set_page_config(
    page_title="KaryaMate",
    page_icon="assets/favicon.ico",
    layout="centered"
)

st.image("assets/logo.png", width=200) 
st.title("KaryaMate — Your Smart Companion for Tasks")
st.write("Welcome to KaryaMate! A modern task manager to keep you organized and focused.")

if st.button("Check Backend Status"):
    try:
        response = requests.get("http://127.0.0.1:5000/health")
        if response.status_code == 200:
            st.success("Backend is running")
        else:
            st.error(f"Backend error: {response.status_code}")
    except Exception as e:
        st.error(f"Cannot connect to backend: {e}")
