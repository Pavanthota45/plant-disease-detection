import streamlit as st
import os
from ml_model.predict import predict_disease
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from ml_model.predict import predict_disease
from backend.db import get_connection

def show_dashboard():

    st.title("🌿 Plant Disease Detection Dashboard")

    st.write(f"Welcome **{st.session_state['user']}**")

    uploaded = st.file_uploader("Upload leaf image", type=["jpg","png","jpeg"])

    if uploaded:

        os.makedirs("uploads", exist_ok=True)
        file_path = os.path.join("uploads", uploaded.name)

        with open(file_path,"wb") as f:
            f.write(uploaded.getbuffer())

        st.image(file_path,width=300)

        # prediction
        disease, confidence = predict_disease(file_path)

        st.success(f"Disease: {disease}")
        st.info(f"Confidence: {confidence*100:.2f}%")

        # store DB
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            "INSERT INTO detections(username,image_path,disease_name,confidence) VALUES(%s,%s,%s,%s)",
            (st.session_state["user"],file_path,disease,confidence)
        )

        conn.commit()
        conn.close()

        st.success("Saved in database")