import streamlit as st

from login import show_login
from signup import show_signup
from forgot_password import show_forgot
from dashboard import show_dashboard
from admin_panel import show_admin

st.set_page_config(page_title="Plant Disease Detection", layout="wide")

# ---------- SESSION ----------
if "user" not in st.session_state:
    st.session_state["user"] = None

menu = ["Login","Signup","Forgot Password","Admin"]

choice = st.sidebar.selectbox("Navigation",menu)

# ---------- ROUTING ----------
if st.session_state["user"]:

    if st.sidebar.button("Logout"):
        st.session_state["user"] = None
        st.rerun()

    show_dashboard()

else:

    if choice == "Login":
        show_login()

    elif choice == "Signup":
        show_signup()

    elif choice == "Forgot Password":
        show_forgot()

    elif choice == "Admin":
        show_admin()