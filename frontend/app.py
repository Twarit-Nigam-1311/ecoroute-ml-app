import streamlit as st
import requests
import pandas as pd

st.set_page_config(page_title="EcoRoute SDE Dashboard", layout="wide")

st.title("🚗 EcoRoute: Fuel Efficiency Predictor")
st.markdown("---")

# User Input Sidebar
st.sidebar.header("Vehicle Parameters")
cyl = st.sidebar.selectbox("Cylinders", [4, 6, 8], index=0)
dis = st.sidebar.slider("Displacement", 50.0, 500.0, 150.0)
hp = st.sidebar.slider("Horsepower", 40.0, 250.0, 100.0)
wt = st.sidebar.number_input("Weight (lbs)", 1500, 5500, 2800)
acc = st.sidebar.slider("Acceleration (0-60)", 8.0, 25.0, 15.0)
yr = st.sidebar.slider("Model Year (70-82)", 70, 82, 76)
org = st.sidebar.radio("Origin", [1, 2, 3], format_func=lambda x: {1:"USA", 2:"Europe", 3:"Japan"}[x])

# Build JSON Payload
payload = {
    "cylinders": cyl, "displacement": dis, "horsepower": hp,
    "weight": wt, "acceleration": acc, "model_year": yr, "origin": org
}

if st.sidebar.button("Run Inference"):
    try:
        response = requests.post("http://127.0.0.1:8000/predict", json=payload)
        if response.status_code == 200:
            result = response.json()["prediction"]
            st.balloons()
            st.metric(label="Predicted Efficiency", value=f"{result} MPG")
        else:
            st.error(f"API Error: {response.json().get('detail')}")
    except Exception as e:
        st.error("Could not connect to Backend. Is Uvicorn running?")

# --- SDE LOGGING SECTION ---
st.markdown("---")
st.subheader("🛠️ Developer Audit Logs")
if st.checkbox("Show Live API Logs"):
    try:
        with open("api_usage.log", "r") as f:
            lines = f.readlines()
            st.code("".join(lines[-10:])) # Show last 10 entries
    except FileNotFoundError:
        st.info("No logs generated yet. Perform a prediction!")