import streamlit as st
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from backend.auth import login_user

def show_login():

    st.title("🔐 Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if login_user(username,password):
            st.session_state["user"] = username
            st.success("Login successful")
            st.rerun()
        else:
            st.error("Invalid credentials")