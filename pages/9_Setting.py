import streamlit as st
from utils.config import init_session_state, save_settings

init_session_state()

st.title("Operations and Settings Dashboard")

st.markdown(
    "Configure global defaults across all operational modules. All configurations persist across page loads."
)

st.header("Default Regional and Model Configurations")

col1, col2 = st.columns(2)

with col1:
  default_country = st.text_input(
      "Default Target Country",
      value=st.session_state.get("default_country", "India"),
  )
  forecast_years = st.slider(
      "Default Forecasting Horizon (Years)",
      1,
      10,
      value=st.session_state.get("forecast_years", 5),
  )

with col2:
  map_style = st.selectbox(
      "Default Map Tile Theme",
      ["Carto Dark", "Carto Positron", "OpenStreetMap"],
      index=["Carto Dark", "Carto Positron", "OpenStreetMap"].index(
          st.session_state.get("map_style", "Carto Dark")
      ),
  )
  confidence_threshold = st.slider(
      "Minimum Prediction Confidence Threshold (%)",
      50,
      100,
      value=st.session_state.get("confidence_threshold", 80),
  )

st.header("Machine Learning Configurations")
show_probability = st.checkbox(
    "Display Full Threat Class Probability Distributions",
    value=st.session_state.get("show_probability", True),
)

st.divider()

if st.button("Save Operational Configuration", type="primary"):
  updated = {
      "default_country": default_country,
      "forecast_years": forecast_years,
      "map_style": map_style,
      "confidence_threshold": confidence_threshold,
      "show_probability": show_probability,
  }
  save_settings(updated)
  for k, v in updated.items():
    st.session_state[k] = v

  st.success("Global Settings successfully updated and saved!")
  st.balloons()