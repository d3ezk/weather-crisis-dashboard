# Import libraries for the UI, maps, API calls, and data visualization
import streamlit as st
from streamlit_folium import st_folium
from weather_api import get_alerts_by_state, get_severity_color
from map_utils import build_alert_map
import plotly.express as px
import pandas as pd

# ─────────────────────────────────────────────
# Page configuration (must be first Streamlit call)
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="Weather Crisis Dashboard",
    page_icon="⛈️",
    layout="wide"
)

# ─────────────────────────────────────────────
# Display app title and description
# ─────────────────────────────────────────────
st.title("⛈️ Weather Crisis Dashboard")
st.markdown("Real-time severe weather alerts across the United States, powered by the National Weather Service.")
st.divider()

# ──────────────────────────────────────────────────────────
# All 50 US states mapped to their 2-letter code for API use
# ──────────────────────────────────────────────────────────
US_STATES = {
    "Alabama": "AL", "Alaska": "AK", "Arizona": "AZ", "Arkansas": "AR",
    "California": "CA", "Colorado": "CO", "Connecticut": "CT", "Delaware": "DE",
    "Florida": "FL", "Georgia": "GA", "Hawaii": "HI", "Idaho": "ID",
    "Illinois": "IL", "Indiana": "IN", "Iowa": "IA", "Kansas": "KS",
    "Kentucky": "KY", "Louisiana": "LA", "Maine": "ME", "Maryland": "MD",
    "Massachusetts": "MA", "Michigan": "MI", "Minnesota": "MN", "Mississippi": "MS",
    "Missouri": "MO", "Montana": "MT", "Nebraska": "NE", "Nevada": "NV",
    "New Hampshire": "NH", "New Jersey": "NJ", "New Mexico": "NM", "New York": "NY",
    "North Carolina": "NC", "North Dakota": "ND", "Ohio": "OH", "Oklahoma": "OK",
    "Oregon": "OR", "Pennsylvania": "PA", "Rhode Island": "RI", "South Carolina": "SC",
    "South Dakota": "SD", "Tennessee": "TN", "Texas": "TX", "Utah": "UT",
    "Vermont": "VT", "Virginia": "VA", "Washington": "WA", "West Virginia": "WV",
    "Wisconsin": "WI", "Wyoming": "WY"
}

# ─────────────────────────────────────────────
# Sidebar filters for user input
# ─────────────────────────────────────────────
st.sidebar.header("🔍 Filter Alerts")

# State selector — defaults to Texas (index 42)
selected_state_name = st.sidebar.selectbox("Select a state", list(US_STATES.keys()), index=42)
state_code = US_STATES[selected_state_name]

# Severity filter — user can uncheck levels they don't want
severity_filter = st.sidebar.multiselect(
    "Filter by severity",
    options=["Extreme", "Severe", "Moderate", "Minor", "Unknown"],
    default=["Extreme", "Severe", "Moderate", "Minor", "Unknown"]
)

# ─────────────────────────────────────────────
# Fetch live alert data from NWS API
# ─────────────────────────────────────────────
with st.spinner(f"Fetching alerts for {selected_state_name}..."):
    all_alerts = get_alerts_by_state(state_code)

# Build alert type filter dynamically from whatever types exist in the data
all_event_types = sorted(set(a["event"] for a in all_alerts)) if all_alerts else []
event_filter = st.sidebar.multiselect(
    "Filter by alert type",
    options=all_event_types,
    default=all_event_types
)

# Apply both filters together
alerts = [
    a for a in all_alerts
    if a["severity"] in severity_filter and a["event"] in event_filter
]

# ─────────────────────────────────────────────
# Summary metric cards at the top
# ─────────────────────────────────────────────
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Alerts", len(alerts))
col2.metric("🔴 Extreme",  sum(1 for a in alerts if a["severity"] == "Extreme"))
col3.metric("🟠 Severe",   sum(1 for a in alerts if a["severity"] == "Severe"))
col4.metric("🟡 Moderate", sum(1 for a in alerts if a["severity"] == "Moderate"))

st.divider()

# ─────────────────────────────────────────────
# Bar chart — alert counts broken down by severity
# ─────────────────────────────────────────────
st.subheader("📊 Alerts by Severity")

if alerts:
    # Count how many alerts exist for each severity level
    severity_order = ["Extreme", "Severe", "Moderate", "Minor", "Unknown"]
    severity_counts = {s: 0 for s in severity_order}
    for a in alerts:
        sev = a["severity"]
        if sev in severity_counts:
            severity_counts[sev] += 1

    # Convert to a DataFrame so plotly can use it
    df_severity = pd.DataFrame({
        "Severity": list(severity_counts.keys()),
        "Count":    list(severity_counts.values())
    })

    # Match bar colors to severity levels
    color_map = {
        "Extreme":  "#d32f2f",
        "Severe":   "#f57c00",
        "Moderate": "#fbc02d",
        "Minor":    "#388e3c",
        "Unknown":  "#757575"
    }
    # Create bar chart
    fig = px.bar(
        df_severity,
        x="Severity",
        y="Count",
        color="Severity",
        color_discrete_map=color_map,
        text="Count",
        title=f"Active Alert Severity Breakdown — {selected_state_name}"
    )
    fig.update_layout(showlegend=False, plot_bgcolor="rgba(0,0,0,0)")
    fig.update_traces(textposition="outside")
    st.plotly_chart(fig, use_container_width=True)

else:
    st.info("No alerts to chart for the current filters.")

st.divider()

# ─────────────────────────────────────────────
# Display Map + Alert list side by side
# ─────────────────────────────────────────────
map_col, list_col = st.columns([1.4, 1])

with map_col:
    st.subheader(f"🗺️ Alert Map — {selected_state_name}")
    # Build and display the folium map with alert polygons
    alert_map = build_alert_map(alerts)
    st_folium(alert_map, width=700, height=450)

with list_col:
    st.subheader(f"📋 Active Alerts ({len(alerts)})")

    if not alerts:
        st.success("✅ No active alerts for this state and severity level.")
    else:
        # Each alert is shown as a clickable expandable card
        for alert in alerts:
            severity = alert["severity"]
            color    = get_severity_color(severity)

            with st.expander(f"🔔 {alert['event']} — {alert['area']}"):
                st.markdown(f"**Severity:** {severity}")
                st.markdown(f"**Certainty:** {alert['certainty']}")
                st.markdown(f"**Area:** {alert['area']}")
                st.markdown(f"**Starts:** {alert['starts']}")
                st.markdown(f"**Expires:** {alert['expires']}")
                st.markdown("---")
                st.markdown(f"**Headline:** {alert['headline']}")
                st.markdown(f"**Description:**\n\n{alert['description']}")

# ─────────────────────────────────────────────
# Footer
# ─────────────────────────────────────────────
st.divider()
st.caption("Data sourced from the National Weather Service API (weather.gov). Refreshes on each interaction.")
