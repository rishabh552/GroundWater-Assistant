
import folium

# Coordinates for key locations in Tamil Nadu (Static geography)
DISTRICT_COORDS = {
    # Northern Districts
    "Chennai": [13.0827, 80.2707],
    "Tiruvallur": [13.1230, 79.9120],
    "Kancheepuram": [12.8342, 79.7036],
    "Chengalpattu": [12.6841, 79.9836],
    "Vellore": [12.9165, 79.1325],
    "Ranipet": [12.9273, 79.3330],
    "Tirupathur": [12.4920, 78.5670],
    "Tiruvannamalai": [12.2330, 79.0667],
    "Villupuram": [11.9398, 79.4920],
    "Kallakurichi": [11.7380, 78.9630],
    
    # West
    "Salem": [11.6643, 78.1460],
    "Erode": [11.3410, 77.7172],
    "Namakkal": [11.2190, 78.1680],
    "Coimbatore": [11.0168, 76.9558],
    "Tiruppur": [11.1085, 77.3411],
    "Nilgiris": [11.4100, 76.6950],
    "Dharmapuri": [12.1277, 78.1578],
    "Krishnagiri": [12.5266, 78.2146],
    
    # Central
    "Tiruchirappalli": [10.7905, 78.7047],
    "Karur": [10.9597, 78.0830],
    "Perambalur": [11.2349, 78.8720],
    "Ariyalur": [11.1400, 79.0780],
    "Pudukkottai": [10.3800, 78.8200],
    "Thanjavur": [10.7870, 79.1378],
    "Thiruvarur": [10.7760, 79.6370],
    "Nagapattinam": [10.7600, 79.8400],
    
    # South
    "Madurai": [9.9252, 78.1198],
    "Dindigul": [10.3673, 77.9803],
    "Theni": [10.0104, 77.4768],
    "Virudhunagar": [9.5680, 77.9624],
    "Sivagangai": [9.8433, 78.4809],
    "Ramanathapuram": [9.3660, 78.8350],
    "Thoothukudi": [8.7642, 78.1348],
    "Tirunelveli": [8.7139, 77.7567],
    "Tenkasi": [8.9660, 77.3000],
    "Kanniyakumari": [8.0883, 77.5385],
}

# Initialize LOCATIONS with coordinates but "Unknown" risk
LOCATIONS = {name: {"coords": coords, "risk": "Unknown"} for name, coords in DISTRICT_COORDS.items()}

# Try to load RAG-generated data if available
try:
    import json
    import os
    if os.path.exists("generated_map_data.json"):
        with open("generated_map_data.json", "r") as f:
            LOCATIONS = json.load(f)
            # print("Loaded dynamic map data from RAG.")
except Exception as e:
    print(f"Using static map data (Error loading dynamic: {e})")

# Color mapping for risk levels
RISK_COLORS = {
    "Safe": "#2ecc71",          # Green
    "Moderate": "#f1c40f",      # Yellow (Alias for Semi-Critical)
    "Semi-Critical": "#f1c40f", # Yellow
    "Critical": "#e67e22",      # Orange
    "Over-Exploited": "#e74c3c",# Red
    "Saline": "#9b59b6"         # Purple
}

def generate_tamil_nadu_map():
    """
    Generates a Folium map centered on Tamil Nadu with risk markers.
    """
    # Center on Tamil Nadu
    m = folium.Map(location=[11.1271, 78.6569], zoom_start=7, tiles="CartoDB dark_matter")
    
    for name, data in LOCATIONS.items():
        risk_level = data["risk"]
        color = RISK_COLORS.get(risk_level, "#95a5a6")
        
        # Create HTML popup content
        popup_html = f"""
        <div style="font-family: Inter, sans-serif; width: 150px;">
            <h4 style="margin: 0; color: #2c3e50;">{name}</h4>
            <p style="margin: 5px 0 0 0; font-size: 12px; color: #7f8c8d;">Status:</p>
            <b style="color: {color}; font-size: 14px;">{risk_level}</b>
        </div>
        """
        
        folium.Marker(
            location=data["coords"],
            popup=folium.Popup(popup_html, max_width=200),
            tooltip=f"{name}: {risk_level}",
            icon=folium.Icon(color="white", icon_color=color, icon="tint", prefix="fa")
        ).add_to(m)
        
        # Add a subtle circle to indicate zone
        folium.Circle(
            location=data["coords"],
            radius=5000, # 5km radius
            color=color,
            fill=True,
            fill_color=color,
            fill_opacity=0.2,
            weight=1
        ).add_to(m)
        
    return m
