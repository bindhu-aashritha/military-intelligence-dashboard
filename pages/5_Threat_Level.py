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

model = joblib.load("models/threat_level_model.pkl")
encoders = joblib.load("models/threat_encoders.pkl")
target_encoder = joblib.load("models/threat_target_encoder.pkl")

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
    c_enc = encoders["country_txt"].transform([country])[0]
    r_enc = encoders["region_txt"].transform([region])[0]
    a_enc = encoders["attacktype1_txt"].transform([attack])[0]
    w_enc = encoders["weaptype1_txt"].transform([weapon])[0]
    t_enc = encoders["targtype1_txt"].transform([target])[0]

    input_df = pd.DataFrame({
        "country_txt": [c_enc],
        "region_txt": [r_enc],
        "attacktype1_txt": [a_enc],
        "weaptype1_txt": [w_enc],
        "targtype1_txt": [t_enc],
        "nkill": [nkill],
        "nwound": [nwound],
    })

    pred = model.predict(input_df)
    probs = model.predict_proba(input_df)[0]
    result = target_encoder.inverse_transform(pred)[0]
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
      prob_df = pd.DataFrame({
          "Threat Class": target_encoder.classes_,
          "Probability": probs,
      })
      st.bar_chart(prob_df.set_index("Threat Class"))

  except Exception as e:
    st.error(f"Prediction Pipeline Error: {str(e)}")