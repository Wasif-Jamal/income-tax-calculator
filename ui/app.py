import streamlit as st
import requests
import os

API_URL = os.getenv("API_URL", "http://localhost:8000")

st.title("Income Tax Calculator")

# Input fields
income = st.number_input("Income", min_value=0.0, step=1000.0)
hra = st.number_input("HRA", min_value=0.0, step=1000.0)
regime = st.selectbox("Regime", ["old", "new"])

# Button
if st.button("Calculate Tax"):
    payload = {
        "income": income,
        "hra": hra,
        "regime": regime
    }

    try:
        response = requests.post(f"{API_URL}/calculate-tax", json=payload)

        if response.status_code == 200:
            data = response.json()
            st.success(f"Tax: ₹ {data['tax']}")
        else:
            st.error(response.json().get("error", "Something went wrong"))

    except Exception as e:
        st.error("API not reachable")