import plotly.express as px
import streamlit as st
from utils.config import init_session_state
from utils.data_loader import load_data

init_session_state()

st.title("Overview")

df = load_data()

st.subheader("Global Security Summary")

c1, c2, c3, c4 = st.columns(4)
c1.metric("Incidents Logged", f"{len(df):,}")
c2.metric("Total Fatalities", f"{int(df['nkill'].sum()):,}")
c3.metric("Total Injured", f"{int(df['nwound'].sum()):,}")
c4.metric("Nations Impacted", df["country_txt"].nunique())

st.divider()

st.subheader("Global Incident Velocity (Historical)")

yearly = df.groupby("iyear").size().reset_index(name="Attacks")

fig = px.line(
    yearly,
    x="iyear",
    y="Attacks",
    markers=True,
    labels={"iyear": "Year", "Attacks": "Total Attacks"},
    template="plotly_dark",
)
fig.update_traces(line_color="#EF553B")

st.plotly_chart(fig, use_container_width=True)