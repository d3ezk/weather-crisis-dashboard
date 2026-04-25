# ⛈️ Weather Crisis Dashboard

A real-time severe weather alert dashboard built with Python and Streamlit, powered by the free National Weather Service API.

## Project Description

This application allows users to explore active severe weather alerts across any U.S. state. Alerts are displayed on an interactive map and as a filterable list, color-coded by severity.

## Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/YOUR_USERNAME/weather-crisis-dashboard.git
   cd weather-crisis-dashboard
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the app:**
   ```bash
   streamlit run app.py
   ```

4. Open your browser to `http://localhost:8501`

## Usage

- Use the sidebar to select any U.S. state
- Filter alerts by severity (Extreme, Severe, Moderate, Minor)
- View alert zones on the interactive map
- Click any alert in the list to expand its full description

## Tech Stack

- **Python** — core language
- **Streamlit** — web app framework
- **Folium** — interactive maps
- **Requests** — HTTP calls to the NWS API
- **National Weather Service API** — free, no API key required

## Team

- [Your Name]
- [Partner Name]
