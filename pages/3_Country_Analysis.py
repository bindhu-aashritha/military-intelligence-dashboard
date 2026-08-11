import plotly.express as px
import streamlit as st
from utils.config import init_session_state
from utils.data_loader import load_data

init_session_state()

st.title("Tactical Country Intelligence Analysis")

df = load_data()

countries = sorted(df["country_txt"].dropna().unique())
default_country = st.session_state.get("default_country", "India")
default_idx = countries.index(default_country) if default_country in countries else 0

country = st.sidebar.selectbox("Select Target Country", countries, index=default_idx)

country_df = df[df["country_txt"] == country]

st.header(f"Intelligence Report: {country}")

c1, c2, c3, c4 = st.columns(4)
c1.metric("Incidents", f"{len(country_df):,}")
c2.metric("Fatalities", f"{int(country_df['nkill'].sum()):,}")
c3.metric("Injured", f"{int(country_df['nwound'].sum()):,}")
c4.metric("Active Groups", country_df["gname"].nunique())

st.divider()

left, right = st.columns(2)

with left:
  yearly = country_df.groupby("iyear").size().reset_index(name="Attacks")
  fig = px.line(
      yearly,
      x="iyear",
      y="Attacks",
      markers=True,
      title="Incident Trend Over Time",
      template="plotly_dark",
  )
  st.plotly_chart(fig, use_container_width=True)

with right:
  attack = country_df.groupby("attacktype1_txt").size().reset_index(name="Count")
  fig = px.pie(
      attack,
      names="attacktype1_txt",
      values="Count",
      title="Attack Tactics Breakdown",
      template="plotly_dark",
  )
  st.plotly_chart(fig, use_container_width=True)

st.divider()

left, right = st.columns(2)

with left:
  groups = (
      country_df.groupby("gname")
      .size()
      .reset_index(name="Attacks")
      .sort_values("Attacks", ascending=False)
      .head(10)
  )
  fig = px.bar(
      groups,
      x="Attacks",
      y="gname",
      orientation="h",
      title="Top Factions and Organizations",
      template="plotly_dark",
  )
  fig.update_layout(yaxis=dict(autorange="reversed"))
  st.plotly_chart(fig, use_container_width=True)

with right:
  weapon = (
      country_df.groupby("weaptype1_txt")
      .size()
      .reset_index(name="Count")
      .sort_values("Count", ascending=False)
  )
  fig = px.bar(
      weapon,
      x="weaptype1_txt",
      y="Count",
      title="Primary Weaponry Utilized",
      template="plotly_dark",
  )
  st.plotly_chart(fig, use_container_width=True)

st.divider()

st.subheader("Tactical Data Ledger")
cols = [
    "iyear",
    "city",
    "attacktype1_txt",
    "targtype1_txt",
    "weaptype1_txt",
    "gname",
    "nkill",
    "nwound",
]
st.dataframe(country_df[cols], use_container_width=True)

csv = country_df.to_csv(index=False).encode("utf-8")
st.download_button(
    "Download Localized Dataset",
    csv,
    file_name=f"{country}_Intelligence_Data.csv",
    mime="text/csv",
)