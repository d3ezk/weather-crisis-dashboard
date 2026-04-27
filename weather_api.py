# Library used to make HTTP requests to the weather API
import requests

# Base URL for the National Weather Service API (free, no API key needed)
BASE_URL = "https://api.weather.gov"

def get_alerts_by_state(state_code):
    """
    Fetch active severe weather alerts for a given US state.
    
    Args:
        state_code (str): Two-letter state abbreviation, e.g. "TX", "FL", "CA"
    
    Returns:
        list: A list of alert dictionaries, or an empty list if none found.
    """

    # Construct API endpoint URL with selected state
    url = f"{BASE_URL}/alerts/active?area={state_code}"
    
    # The NWS API requires a User-Agent header — they use it to contact you if needed
    headers = {
        "User-Agent": "WeatherCrisisDashboard/1.0 (your_email@example.com)"
    }
    
    try:
        # Send GET request to API
        response = requests.get(url, headers=headers, timeout=10)
        # Raises an error if the request failed
        response.raise_for_status()
        # Convert response to JSON format
        data = response.json()
        # Extract alert list from response
        alerts = data.get("features", [])
        # Parse out only the fields we care about
        parsed = []
        for alert in alerts:
            props = alert.get("properties", {})
            parsed.append({
                "event":       props.get("event", "Unknown Event"),
                "severity":    props.get("severity", "Unknown"),
                "certainty":   props.get("certainty", "Unknown"),
                "headline":    props.get("headline", "No headline available"),
                "description": props.get("description", "No description available"),
                "area":        props.get("areaDesc", "Unknown Area"),
                "starts":      props.get("onset", "N/A"),
                "expires":     props.get("expires", "N/A"),
                "geometry":    alert.get("geometry")  # Used for mapping
            })
        
        return parsed
    # Handle request timeout separately
    except requests.exceptions.Timeout:
        print("Request timed out. Check your internet connection.")
        return []
    # Handle all other request related errors
    except requests.exceptions.RequestException as e:
        print(f"Error fetching alerts: {e}")
        return []


def get_severity_color(severity):
    """
    Return a color string based on alert severity.
    Used for color-coding alerts in the UI.
    """
    # Mapping of severity levels to colors for consistent UI styling
    colors = {
        "Extreme":  "#d32f2f",  # Red
        "Severe":   "#f57c00",  # Orange
        "Moderate": "#fbc02d",  # Yellow
        "Minor":    "#388e3c",  # Green
        "Unknown":  "#757575",  # Gray
    }
    # Return matching color but default to gray if unknown
    return colors.get(severity, "#757575")
