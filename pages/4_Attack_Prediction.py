import os
import joblib
import pandas as pd
import streamlit as st
from utils.config import init_session_state
from utils.data_loader import load_data

init_session_state()

st.title("Tactical Attack Vector Prediction")

st.markdown(
    "Input mission variables to predict the probable Attack Tactics using the pre-trained Machine Learning model."
)

if not os.path.exists("models/attack_prediction_model.pkl"):
  st.error(
      "Models not initialized! Please execute `python train_models.py` in your terminal first."
  )
  st.stop()

pipeline = joblib.load("models/attack_prediction_model.pkl")

df = load_data().dropna(
    subset=[
        "country_txt",
        "region_txt",
        "weaptype1_txt",
        "targtype1_txt",
        "gname",
    ]
)

with st.form("prediction_form"):
  col1, col2 = st.columns(2)

  with col1:
    country = st.selectbox("Country", sorted(df["country_txt"].unique()))
    region = st.selectbox("Region", sorted(df["region_txt"].unique()))
    weapon = st.selectbox(
        "Weapon Type", sorted(df["weaptype1_txt"].unique())
    )
    target = st.selectbox(
        "Target Category", sorted(df["targtype1_txt"].unique())
    )

  with col2:
    group = st.selectbox("Terrorist Faction", sorted(df["gname"].unique()))
    success = st.selectbox(
        "Attack Success Expected?",
        [1, 0],
        format_func=lambda x: "Yes" if x == 1 else "No",
    )
    suicide = st.selectbox(
        "Suicide Tactical Mission?",
        [1, 0],
        format_func=lambda x: "Yes" if x == 1 else "No",
    )
  submitted = st.form_submit_button("Execute Prediction Model")

if submitted:
  try:
    input_df = pd.DataFrame({
        "country_txt": [country],
        "region_txt": [region],
        "weaptype1_txt": [weapon],
        "targtype1_txt": [target],
        "gname": [group],
        "success": [success],
        "suicide": [suicide],
    })

    attack_type = pipeline.predict(input_df)[0]
    probs = pipeline.predict_proba(input_df)
    confidence = probs.max() * 100
    st.subheader("Intelligence Assessment")
    st.success(f"Predicted Attack Vector: {attack_type}")
    st.metric("Model Confidence Score", f"{confidence:.2f}%")

  except Exception as e:
    st.error(f"Error executing model: {str(e)}")