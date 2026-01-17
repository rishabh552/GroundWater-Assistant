import json
from pathlib import Path
from fastapi import APIRouter, HTTPException

router = APIRouter()

# Path to the data file (relative to project root)
# api/routes is 2 levels deep from root, but execution context matters.
# Assuming run from root via uvicorn api.main:app
DATA_FILE = Path("generated_map_data.json")

@router.get("/map")
async def get_map_data():
    """
    Serve the pre-generated map data (Coordinates + Risk Levels).
    """
    if not DATA_FILE.exists():
        raise HTTPException(status_code=404, detail="Map data not found. Please run update_map_risks.py first.")
    
    try:
        with open(DATA_FILE, "r") as f:
            data = json.load(f)
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error reading map data: {str(e)}")
