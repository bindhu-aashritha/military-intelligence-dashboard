import plotly.express as px
import streamlit as st
from utils.config import init_session_state
from utils.data_loader import load_data

init_session_state()

st.title("Global Threat Map")

df = load_data()

st.sidebar.header("Map Configurations")
#Added Map View Mode selector (Scatter vs. Density Mapbox)
map_view_type = st.sidebar.radio(
    "Select Visualization Mode",
    ["Scatter Map (Events)", "Density Map (Hotspots)"],
)

year = st.sidebar.selectbox(
    "Select Year", ["All"] + sorted(df["iyear"].unique().tolist(), reverse=True)
)

if year != "All":
  df = df[df["iyear"] == year]

map_df = df.dropna(subset=["latitude", "longitude"])

style_map = {
    "Carto Dark": "carto-darkmatter",
    "Carto Positron": "carto-positron",
    "OpenStreetMap": "open-street-map",
}
selected_style = style_map.get(
    st.session_state.get("map_style", "Carto Dark"), "carto-darkmatter"
)

#Conditional map rendering based on selected mode
if map_view_type == "Scatter Map (Events)":
   fig = px.scatter_mapbox(
    map_df,
    lat="latitude",
    lon="longitude",
    color="attacktype1_txt",
    hover_name="country_txt",
    hover_data=["city", "gname", "nkill"],
    zoom=1,
    height=700,
    mapbox_style=selected_style,
    title=f"Geospatial Attack Distribution ({'All Years' if year == 'All' else year})",
)
else:
  #Density Mapbox hotspot visualization
  fig = px.density_mapbox(
      map_df,
      lat="latitude",
      lon="longitude",
      z="nkill",  # Weighted by fatality impact
      radius=10,
      zoom=1,
      height=700,
      mapbox_style=selected_style,
      title=(
          f"Threat Density & Hotspot Assessment ({'All Years' if year == 'All' else year})"
      ),
  )

fig.update_layout(margin=dict(l=0, r=0, t=40, b=0))

st.plotly_chart(fig, use_container_width=True)