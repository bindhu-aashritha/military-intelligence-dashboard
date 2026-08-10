import streamlit as st
from utils.config import init_session_state

st.set_page_config(
    page_title="AI Military Intelligence Dashboard", layout="wide"
)

init_session_state()

st.title("AI-Based Military Intelligence Dashboard")

st.markdown("""
### Tactical Command and Threat Analytics Portal

This dashboard provides actionable military intelligence analysis using the Global Terrorism Database (GTD).

#### Modules Available
* Home: High-level strategic metrics and multi-year threat overview.
* Global Threat Map: Interactive geospatial heatmaps and geospatial density layers.
* Country Analysis: In-depth tactical reports on localized threats, factions, and target profiles.
* Attack Prediction: Machine Learning classifier to predict probable tactical attack vectors.
* Threat Level: Predictive impact categorization model (Low, Medium, High).
* Forecasting: Long-term strategic projections and multi-year trajectory estimations.
* AI Intelligence: Automated Executive Summaries and Situational Reports (SITREPs).
* Data Explorer: Deep-dive queries, multidimensional filtering, and raw dataset exports.
* Settings: Persistent user settings and model configuration thresholds.

---
Select a module from the left sidebar navigation to begin.
""")