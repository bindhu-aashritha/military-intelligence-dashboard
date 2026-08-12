import os
import joblib
import pandas as pd
import streamlit as st
from utils.config import init_session_state
from utils.data_loader import load_data

init_session_state()

st.title("Threat Level Assessment Model")

if not os.path.exists("models/threat_level_model.pkl"):
  st.error("Model files missing. Please run `python train_models.py` offline first.")
  st.stop()

pipeline = joblib.load("models/threat_level_model.pkl")

df = load_data()

st.sidebar.header("Incident Vector Parameters")

country = st.sidebar.selectbox(
    "Country Target", sorted(df["country_txt"].dropna().unique())
)
region = st.sidebar.selectbox(
    "Region Target", sorted(df["region_txt"].dropna().unique())
)
attack = st.sidebar.selectbox(
    "Attack Type", sorted(df["attacktype1_txt"].dropna().unique())
)
weapon = st.sidebar.selectbox(
    "Weapon Type", sorted(df["weaptype1_txt"].dropna().unique())
)
target = st.sidebar.selectbox(
    "Target Category", sorted(df["targtype1_txt"].dropna().unique())
)

nkill = st.sidebar.number_input("Estimated Fatalities", 0, 10000, 0)
nwound = st.sidebar.number_input("Estimated Injured", 0, 10000, 0)

if st.sidebar.button("Compute Threat Index"):
  try:
    input_df = pd.DataFrame({
        "country_txt": [country],
        "region_txt": [region],
        "attacktype1_txt": [attack],
        "weaptype1_txt": [weapon],
        "targtype1_txt": [target],
        "nkill": [nkill],
        "nwound": [nwound],
    })

    result = pipeline.predict(input_df)[0]
    probs = pipeline.predict_proba(input_df)[0]
    confidence = probs.max() * 100

    st.subheader("Computed Threat Level Result")

    if result == "LOW":
      st.success(f"Threat Level: {result}")
    elif result == "MEDIUM":
      st.warning(f"Threat Level: {result}")
    else:
      st.error(f"Threat Level: {result}")

    st.metric("Model Confidence Score", f"{confidence:.2f}%")

    if st.session_state.get("show_probability", True):
      st.subheader("Threat Probability Distribution")
      prob_df = pd.DataFrame(
          {"Threat Class": pipeline.classes_, "Probability": probs}
      )
      st.bar_chart(prob_df.set_index("Threat Class"))

  except Exception as e:
    st.error(f"Prediction Pipeline Error: {str(e)}")