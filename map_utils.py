import folium

def build_alert_map(alerts):
    """
    Build a folium map showing alert zones for the given list of alerts.

    Args:
        alerts (list): List of parsed alert dicts from weather_api.py

    Returns:
        folium.Map: A map object that Streamlit can render.
    """
    # Start centered on the continental US
    m = folium.Map(location=[38.0, -96.0], zoom_start=4, tiles="CartoDB positron")

    # Color map for severity levels
    severity_colors = {
        "Extreme":  "red",
        "Severe":   "orange",
        "Moderate": "beige",
        "Minor":    "green",
        "Unknown":  "gray",
    }

    for alert in alerts:
        severity = alert.get("severity", "Unknown")
        color    = severity_colors.get(severity, "gray")
        area     = alert.get("area", "Unknown Area")
        event    = alert.get("event", "Weather Alert")
        geometry = alert.get("geometry")

        if geometry:
            # If the alert has polygon coordinates, draw it on the map
            try:
                folium.GeoJson(
                    geometry,
                    style_function=lambda feat, c=color: {
                        "fillColor":   c,
                        "color":       c,
                        "weight":      2,
                        "fillOpacity": 0.35,
                    },
                    tooltip=f"{event} — {area}"
                ).add_to(m)
            except Exception:
                pass  # Skip alerts with malformed geometry

    return m
