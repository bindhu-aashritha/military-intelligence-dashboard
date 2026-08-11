import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st
from sklearn.linear_model import LinearRegression
from utils.config import init_session_state
from utils.data_loader import load_data

init_session_state()

st.title("Long-Term Attack Forecasting Engine")

df = load_data()

st.sidebar.header("Forecast Configurations")

countries = sorted(df["country_txt"].dropna().unique())
default_country = st.session_state.get("default_country", "India")
default_idx = countries.index(default_country) if default_country in countries else 0

country = st.sidebar.selectbox("Target Country", countries, index=default_idx)
forecast_horizon = st.sidebar.slider(
    "Forecast Horizon (Years)",
    1,
    10,
    st.session_state.get("forecast_years", 5),
)

country_df = df[df["country_txt"] == country]

yearly = (
    country_df.groupby("iyear").size().reset_index(name="Attacks").sort_values("iyear")
)

if len(yearly) < 5:
  st.warning("Insufficient historical data points to generate reliable trend forecasts.")
  st.stop()

yearly["iyear_sq"] = yearly["iyear"] ** 2
X = yearly[["iyear", "iyear_sq"]]
y = yearly["Attacks"]

model = LinearRegression()
model.fit(X, y)

last_year = int(yearly["iyear"].max())
future_years = np.arange(last_year + 1, last_year + forecast_horizon + 1)
future_df = pd.DataFrame(
    {"iyear": future_years, "iyear_sq": future_years**2}
)

predictions = model.predict(future_df)
predictions = np.maximum(predictions, 0)

forecast = pd.DataFrame({
    "Year": future_years,
    "Forecasted Attacks": predictions.astype(int),
})

fig = go.Figure()
fig.add_trace(
    go.Scatter(
        x=yearly["iyear"],
        y=yearly["Attacks"],
        mode="lines+markers",
        name="Historical Observed",
    )
)
fig.add_trace(
    go.Scatter(
        x=forecast["Year"],
        y=forecast["Forecasted Attacks"],
        mode="lines+markers",
        name="Predictive Trajectory",
        line=dict(dash="dash", color="red"),
    )
)
fig.update_layout(
    title=f"Attack Trend Projection for {country}",
    xaxis_title="Year",
    yaxis_title="Incidents",
    template="plotly_dark",
    height=550,
)

st.plotly_chart(fig, use_container_width=True)

st.subheader("Forecasted Metrics")
st.dataframe(forecast, use_container_width=True)

historical_last = yearly.iloc[-1]["Attacks"]
forecast_last = forecast.iloc[-1]["Forecasted Attacks"]
growth = ((forecast_last - historical_last) / max(historical_last, 1)) * 100

col1, col2, col3 = st.columns(3)
col1.metric("Recent Observed Annual Attacks", int(historical_last))
col2.metric(f"Projected (+{forecast_horizon} Years)", int(forecast_last))
col3.metric("Projected Growth %", f"{growth:.2f}%")