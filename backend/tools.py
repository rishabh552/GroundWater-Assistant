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

def web_search(query: str) -> str:
    """
    Search the web for real-time information using DuckDuckGo.
    
    Args:
        query (str): The search query.
        
    Returns:
        str: Summary of search results.
    """
    try:
        from duckduckgo_search import DDGS
        
        print(f"Searching web for: {query}")
        
        # We use a context manager as recommended for DDGS
        with DDGS() as ddgs:
            # OPTIMIZATION: Reduce max_results from 10 to 5 for speed
            results = list(ddgs.text(query, region='in-en', max_results=5))
            
            # 2. Fallback to news if text search returns nothing (common for local data)
            if not results:
                print(f"No text results for '{query}', trying news fallback...")
                results = list(ddgs.news(query, region='in-en', max_results=3))
        
        if not results:
            return (
                "No web results found. Ground water data for specific regions in TN is often strictly regulated and may not be publicly updated online."
            )
            
        formatted_results = f"🌐 **Live Web Context:**\n"
        for i, res in enumerate(results, 1):
            source_body = res.get('body') or res.get('snippet') or "No description."
            formatted_results += f"{i}. {res['title']}: {source_body}\n"
            
        return formatted_results
        
    except Exception as e:
        error_msg = str(e)
        if "Ratelimit" in error_msg:
            return (
                "⚠️ **Web Search is temporarily busy (Rate Limited).** "
                "I will proceed using the available technical reports and my internal knowledge base. "
                "Please try again in a few minutes for real-time web results."
            )
        return f"Web search failed: {error_msg}"

def check_well_spacing(risk_category: str) -> str:
    """
    Check minimal spacing requirements between borewells in Tamil Nadu.
    
    Args:
        risk_category (str): The official risk status (Safe, Semi-Critical, Critical, Over-Exploited).
        
    Returns:
        str: Spacing and legal requirements.
    """
    risk = risk_category.lower()
    
    base_info = (
        "📍 **Standard Spacing Rules (Tamil Nadu):**\n"
        "- **Min Distance**: 200 meters (approx 660 ft) from the nearest irrigation well.\n"
        "- **Drinking Water Source**: Must be at least 50 meters away from any public drinking water source.\n"
    )
    
    if "over-exploited" in risk or "critical" in risk:
        return (
            base_info +
            "⚠️ **STRICT REGULATION**: In your zone, construction of new wells is restricted. "
            "You MUST obtain a No Objection Certificate (NOC) from the District Collector / Ground Water Authority. "
            "Drilling without permission may lead to rig seizure and electricity disconnection."
        )
    elif "semi-critical" in risk:
        return (
            base_info +
            "🟠 **CAUTION**: Regulations are tighter here. Ensure your well is registered with the Ground Water Authority immediately after drilling."
        )
    else:
        return (
            base_info +
            "🟢 **GENERAL**: Standard spacing of 200m applies. Registration is mandatory but approvals are generally simpler in Safe zones."
        )

def navigator_groundwater_schemes(farmer_type: str, risk_category: str) -> str:
    """
    Recommend government schemes based on farmer profile and location.
    
    Args:
        farmer_type (str): "small", "marginal", "sc_st", or "general".
        risk_category (str): Safe, Semi-Critical, Critical, Over-Exploited.
        
    Returns:
        str: List of recommended schemes.
    """
    farmer = farmer_type.lower()
    risk = risk_category.lower()
    
    schemes = "📜 **Recommended Government Schemes (Tamil Nadu):**\n"
    
    if "sc" in farmer or "st" in farmer or "marginal" in farmer or "small" in farmer:
        schemes += "- **Million Wells Scheme (MGNREGA)**: Provides up to 100% subsidy for well construction for eligible small/marginal and SC/ST farmers.\n"
    
    schemes += "- **PMKSY (Per Drop More Crop)**: Providing 75% to 100% subsidy for Drip/Sprinkler irrigation systems. Mandatory for new power connections in many blocks.\n"
    schemes += "- **TN Free Agricultural Electricity**: Standard free power connection. Note: Expect a waiting period unless using the 'Tatkal' scheme.\n"
    
    if "over-exploited" in risk:
        schemes += "- **Kalaignarin Integrated Agri Development**: Focuses on community borewells and water harvesting in stressed blocks.\n"
        
    schemes += "\n💡 **Tip**: Visit your local Agricultural Engineering Department (AED) office to apply."
    return schemes

def calculate_pumping_requirements(depth_ft: int) -> str:
    """
    Calculate required Horsepower (HP) for a submersible pump based on depth.
    
    Args:
        depth_ft (int): Total depth of the well in feet.
        
    Returns:
        str: Technical pumping requirements.
    """
    # Simple engineering approximation for small-hold irrigation
    # Total Head = Static Head (depth) + Elevation + Friction (approx 15%)
    total_head = depth_ft * 1.15
    
    # Standard HP buckets for TN farmers
    if depth_ft < 150:
        hp = 3.0
    elif depth_ft < 300:
        hp = 5.0
    elif depth_ft < 600:
        hp = 7.5
    elif depth_ft < 1000:
        hp = 10.0
    else:
        hp = 12.5
        
    return (
        f"⚙️ **Pumping Requirements for {depth_ft}ft Depth:**\n"
        f"- **Recommended Motor**: {hp} HP Submersible Pump.\n"
        f"- **Design Strategy**: Ensure a 'High Head' pump model is selected.\n"
        f"- **Casing Suggestion**: At least top 60-100ft must be cased to prevent collapse.\n"
        f"⚠️ *Consult a local hydrogeologist or licensed driller for exact geophysical site selection.*"
    )

def comprehensive_district_report(location: str, risk_category: str, farmer_type: str = "general") -> str:
    """
    Aggregated tool that provides Spacing, Schemes, and Pumping data in ONE call.
    Use this as the FIRST action after identifying the location/risk.
    
    Args:
        location (str): Name of the block/district.
        risk_category (str): Safe, Semi-Critical, Critical, Over-Exploited.
        farmer_type (str): small, marginal, sc_st, or general.
    """
    spacing = check_well_spacing(risk_category)
    schemes = navigator_groundwater_schemes(farmer_type, risk_category)
    
    # We use a default depth of 500ft for the initial aggregated report 
    # unless the user specifies otherwise.
    pumping = calculate_pumping_requirements(500) 
    
    return (
        f"📊 **COMPREHENSIVE ANALYSIS FOR {location.upper()} ({risk_category.upper()}):**\n\n"
        f"{spacing}\n\n"
        f"{schemes}\n\n"
        f"⚙️ **Standard Gear Recommendation (assuming ~500ft):**\n"
        f"{pumping}\n"
        "\n*Note: Use specific tools like `estimate_borewell_cost` or `calculate_pumping_requirements` for deeper/custom needs.*"
    )

# List of available tools for the Agent to see
AVAILABLE_TOOLS = {
    "estimate_borewell_cost": estimate_borewell_cost,
    "check_crop_feasibility": check_crop_feasibility,
    "web_search": web_search,
    "check_well_spacing": check_well_spacing,
    "navigator_groundwater_schemes": navigator_groundwater_schemes,
    "calculate_pumping_requirements": calculate_pumping_requirements,
    "comprehensive_district_report": comprehensive_district_report
}
