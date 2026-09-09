import streamlit as st
import pandas as pd
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from backend.db import get_connection
def show_admin():

    st.title("👨‍💻 Admin Panel")

    conn = get_connection()

    st.subheader("Registered Users")
    users = pd.read_sql("SELECT id,username,email FROM users",conn)
    st.dataframe(users)

    st.subheader("Detection History")
    detections = pd.read_sql("SELECT * FROM detections",conn)
    st.dataframe(detections)

    conn.close()