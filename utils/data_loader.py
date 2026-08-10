from pathlib import Path
import pandas as pd
import streamlit as st

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_DIR / "data" / "globalterrorism.csv"


@st.cache_data(show_spinner="Loading Global Terrorism Database...")
def load_data():
  df = pd.read_csv(DATA_PATH, encoding="latin1", low_memory=False)
  df["nkill"] = pd.to_numeric(df["nkill"], errors="coerce").fillna(0)
  df["nwound"] = pd.to_numeric(df["nwound"], errors="coerce").fillna(0)
  df["iyear"] = pd.to_numeric(df["iyear"], errors="coerce")
  return df