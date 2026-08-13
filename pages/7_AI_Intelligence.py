import plotly.express as px
import streamlit as st
from utils.config import init_session_state
from utils.data_loader import load_data
from datetime import datetime

init_session_state()

st.title("Automated AI Situation Report (SITREP)")

df = load_data()

st.sidebar.header("Filter Scope")
years = sorted(df["iyear"].unique(), reverse=True)
selected_year = st.sidebar.selectbox("Select Target Year", ["All"] + list(years))

if selected_year != "All":
  df = df[df["iyear"] == selected_year]

total_incidents = len(df)
total_killed = int(df["nkill"].sum())
total_wounded = int(df["nwound"].sum())
countries_count = df["country_txt"].nunique()

top_countries = df["country_txt"].value_counts().head(5)
top_groups = df["gname"].value_counts().head(5)
top_attacks = df["attacktype1_txt"].value_counts().head(5)
top_weapons = df["weaptype1_txt"].value_counts().head(5)

#Generated automated ISO timestamp
timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")

st.subheader("Executive Situation Briefing")

#Refactored SITREP text with timestamped headers & professional formatting
sitrep_text =f"""### CONFIDENTIAL // DEFENSE INTELLIGENCE SUMMARY(SITREP)

**GENERATED TIMESTAMP:** `{timestamp}`  
**TEMPORAL SCOPE:** `{selected_year if selected_year != 'All' else 'Historical Aggregated'}`  
**SECURITY CLASSIFICATION:** RESTRICTED / INTERNAL EVALUATION  

---

### 1. OPERATIONAL QUANTITATIVE METRICS
* **Total Recorded Kinetic Events:** {total_incidents:,}
* **Fatalities:** {total_killed:,}
* **Casualties Wounded:** {total_wounded:,}
* **Affected Sovereignty Areas:** {countries_count} Nations

---

### 2. PRIMARY OPERATIONAL INSIGHTS
1. **Primary High-Risk Area:** `{top_countries.index[0]}` leading incident occurrences with `{top_countries.iloc[0]:,}` recorded events.
2. **Dominant Faction/Group:** `{top_groups.index[0]}` identified as the primary active threat actor.
3. **Primary Tactical Vector:** `{top_attacks.index[0]}` constitutes the majority of incident methods.
4. **Primary Weaponry Category:** `{top_weapons.index[0]}` logged as the dominant weapon utilized.

---

### 3. TACTICAL RISK DISTRIBUTION
* **Top 3 High-Impact Countries:** {', '.join(top_countries.index[:3])}
* **Top 3 Factions:** {', '.join(top_groups.index[:3])}
* **Primary Threat Vector:** {top_attacks.index[0]}
"""

st.info(sitrep_text)

c1, c2 = st.columns(2)

with c1:
  st.subheader("Top High-Risk Countries")
  fig = px.bar(
      top_countries,
      x=top_countries.values,
      y=top_countries.index,
      orientation="h",
      template="plotly_dark",
  )
  fig.update_layout(yaxis=dict(autorange="reversed"))
  st.plotly_chart(fig, use_container_width=True)

with c2:
  st.subheader("Top Active Factions")
  fig2 = px.bar(
      top_groups,
      x=top_groups.values,
      y=top_groups.index,
      orientation="h",
      template="plotly_dark",
  )
  fig2.update_layout(yaxis=dict(autorange="reversed"))
  st.plotly_chart(fig2, use_container_width=True)

#Added dual export capabilities (.md and .txt formats)
col_dl1, col_dl2 = st.columns(2)

with col_dl1:
  st.download_button(
    "Export SITREP Briefing (.MD)",
    sitrep_text,
    file_name=f"SITREP_{selected_year}_{datetime.utcnow().strftime('%Y%m%d')}.md",
    mime="text/markdown",
  )
with col_dl2:
  st.download_button(
      "Export Raw Text SITREP (.TXT)",
      sitrep_text,
      file_name=f"SITREP_{selected_year}_{datetime.utcnow().strftime('%Y%m%d')}.txt",
      mime="text/plain",
  )