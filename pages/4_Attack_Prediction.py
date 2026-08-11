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

model = joblib.load("models/attack_prediction_model.pkl")
encoders = joblib.load("models/feature_encoders.pkl")
target_encoder = joblib.load("models/target_encoder.pkl")

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
    c_enc = encoders["country_txt"].transform([country])[0]
    r_enc = encoders["region_txt"].transform([region])[0]
    w_enc = encoders["weaptype1_txt"].transform([weapon])[0]
    t_enc = encoders["targtype1_txt"].transform([target])[0]
    g_enc = encoders["gname"].transform([group])[0]

    input_df = pd.DataFrame({
        "country_txt": [c_enc],
        "region_txt": [r_enc],
        "weaptype1_txt": [w_enc],
        "targtype1_txt": [t_enc],
        "gname": [g_enc],
        "success": [success],
        "suicide": [suicide],
    })

    prediction = model.predict(input_df)
    probs = model.predict_proba(input_df)

    attack_type = target_encoder.inverse_transform(prediction)[0]
    confidence = probs.max() * 100

    st.subheader("Intelligence Assessment")
    st.success(f"Predicted Attack Vector: {attack_type}")
    st.metric("Model Confidence Score", f"{confidence:.2f}%")

  except Exception as e:
    st.error(f"Error executing model: {str(e)}")