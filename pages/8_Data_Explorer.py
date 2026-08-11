import plotly.express as px
import streamlit as st
from utils.config import init_session_state
from utils.data_loader import load_data

init_session_state()

st.title("Global Terrorism Data Explorer")

df = load_data()

st.sidebar.header("Filter Dataset")

selected_year = st.sidebar.multiselect(
    "Select Year", sorted(df["iyear"].unique()), default=[]
)
selected_country = st.sidebar.multiselect(
    "Select Country", sorted(df["country_txt"].dropna().unique()), default=[]
)
selected_attack = st.sidebar.multiselect(
    "Select Attack Type",
    sorted(df["attacktype1_txt"].dropna().unique()),
    default=[],
)

filtered_df = df.copy()

if selected_year:
  filtered_df = filtered_df[filtered_df["iyear"].isin(selected_year)]
if selected_country:
  filtered_df = filtered_df[filtered_df["country_txt"].isin(selected_country)]
if selected_attack:
  filtered_df = filtered_df[
      filtered_df["attacktype1_txt"].isin(selected_attack)
  ]

search = st.text_input("Substring Search by City or Faction")

if search:
  filtered_df = filtered_df[
      filtered_df["city"].fillna("").str.contains(search, case=False)
      | filtered_df["gname"].fillna("").str.contains(search, case=False)
  ]

st.subheader("Dataset Summary Metrics")
c1, c2, c3, c4 = st.columns(4)
c1.metric("Filtered Records", f"{len(filtered_df):,}")
c2.metric("Nations Covered", filtered_df["country_txt"].nunique())
c3.metric("Total Fatalities", f"{int(filtered_df['nkill'].sum()):,}")
c4.metric("Total Injured", f"{int(filtered_df['nwound'].sum()):,}")

st.dataframe(filtered_df, use_container_width=True, height=450)

csv = filtered_df.to_csv(index=False).encode("utf-8")
st.download_button(
    "Download Filtered Slice CSV",
    csv,
    file_name="Filtered_GTD_Data.csv",
    mime="text/csv",
)