import streamlit as st
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from backend.auth import register_user
def show_signup():

    st.title("📝 Signup")

    username = st.text_input("Username")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Create Account"):
        register_user(username,email,password)
        st.success("Account created successfully! Please login.")