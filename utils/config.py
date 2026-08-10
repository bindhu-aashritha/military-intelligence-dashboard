import json
import os
import streamlit as st

CONFIG_FILE = "config.json"

DEFAULT_SETTINGS = {
    "theme": "Dark",
    "default_country": "India",
    "forecast_years": 5,
    "confidence_threshold": 80,
    "map_style": "Carto Dark",
    "forecast_model": "Prophet / Trend Decomposition",
    "ml_model": "Random Forest",
    "show_probability": True,
}


def load_settings():
  if os.path.exists(CONFIG_FILE):
    try:
      with open(CONFIG_FILE, "r") as f:
        return json.load(f)
    except Exception:
      return DEFAULT_SETTINGS.copy()
  return DEFAULT_SETTINGS.copy()


def save_settings(settings_dict):
  with open(CONFIG_FILE, "w") as f:
    json.dump(settings_dict, f, indent=4)


def init_session_state():
  settings = load_settings()
  for key, value in settings.items():
    if key not in st.session_state:
      st.session_state[key] = value