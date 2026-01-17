"""
Jal-Rakshak Agent Tools
These functions are the "hands" of the agent, allowing it to perform calculations and lookups.
"""
import json

def estimate_borewell_cost(depth_ft: int) -> str:
    """
    Estimate the cost of drilling a borewell based on depth.
    
    Args:
        depth_ft (int): Depth in feet.
        
    Returns:
        str: JSON string with cost breakdown.
    """
    # Standard rates in Tamil Nadu (approximate)
    drilling_rate = 90  # Rs per foot
    casing_rate = 350   # Rs per foot (usually top 60-100ft)
    pump_cost = 25000   # Base cost for reliable submersible pump
    misc_cost = 10000   # Transport, labor, permission
    
    # Calculation
    drilling_cost = depth_ft * drilling_rate
    casing_length = min(depth_ft, 100) # Casing usually needed only for top soil
    casing_cost = casing_length * casing_rate
    
    total_cost = drilling_cost + casing_cost + pump_cost + misc_cost
    
    # Return a readable string instead of JSON to avoid Unicode issues
    result = (
        f"**Estimated Cost for {depth_ft}ft Borewell:** ₹{total_cost:,}\n"
        f"- Drilling: ₹{drilling_cost:,}\n"
        f"- Casing: ₹{casing_cost:,} (approx {casing_length}ft)\n"
        f"- Pump & Motor: ₹{pump_cost:,}\n"
        f"- Misc (Labor/Transport): ₹{misc_cost:,}"
    )
    
    return result

def check_crop_feasibility(water_depth_m: float, crop_name: str) -> str:
    """
    Check if a crop is feasible given the groundwater depth.
    
    Args:
        water_depth_m (float): Groundwater depth in meters (below ground level).
        crop_name (str): Name of the crop (e.g., "paddy", "coconut").
        
    Returns:
        str: Feasibility assessment.
    """
    crop_name = crop_name.lower()
    
    # Water requirement categories
    high_water_crops = ["paddy", "rice", "sugarcane", "banana", "turmeric"]
    medium_water_crops = ["coconut", "arecanut", "cotton", "maize", "vegetables", "tomato", "chilli"]
    low_water_crops = ["millets", "pulses", "ragi", "groundnut", "gingelly", "sorghum"]
    
    if water_depth_m > 20: # Very deep / scarce water
        if any(c in crop_name for c in high_water_crops):
            return "NOT RECOMMENDED: High water requirement crop. Water level is too deep (>20m). Risk of crop failure and high pumping costs."
        elif any(c in crop_name for c in medium_water_crops):
            return "RISKY: Only recommended with Drip Irrigation. Water is deep."
        else:
            return "FEASIBLE: Low water crop suitable for this depth."
            
    elif water_depth_m > 10: # Moderate depth
        if any(c in crop_name for c in high_water_crops):
            return "CAUTION: Feasible but requires good water management. Consider alternatives if monsoon fails."
        else:
            return "FEASIBLE: Good condition for this crop."
            
    else: # Shallow water (Safe zone)
        return "HIGHLY FEASIBLE: Water availability is good for this crop."

# List of available tools for the Agent to see
AVAILABLE_TOOLS = {
    "estimate_borewell_cost": estimate_borewell_cost,
    "check_crop_feasibility": check_crop_feasibility
}
