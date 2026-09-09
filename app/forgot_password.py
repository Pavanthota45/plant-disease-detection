import streamlit as st
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from backend.auth import reset_password

def show_forgot():

    st.title("🔑 Forgot Password")

    username = st.text_input("Enter Username")
    new_password = st.text_input("New Password", type="password")

    if st.button("Reset Password"):
        reset_password(username,new_password)
        st.success("Password updated successfully!")