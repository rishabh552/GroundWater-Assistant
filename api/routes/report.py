"""
Report endpoint for Jal-Rakshak API
Generates PDF reports for queries
"""
import sys
import os

# Add parent directory to path for backend imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from fastapi import APIRouter, HTTPException
from fastapi.responses import Response
from pydantic import BaseModel

from backend.report_generator import create_pdf

router = APIRouter()

class ReportRequest(BaseModel):
    query: str
    location: str
    risk_level: str
    full_response: str

@router.post("/report")
async def generate_report(request: ReportRequest):
    """Generate a PDF report for a query."""
    try:
        # Validate inputs
        if not request.query or not request.full_response:
            raise HTTPException(status_code=400, detail="Query and full_response are required")
        
        pdf_bytes = create_pdf(
            query=request.query,
            location=request.location,
            risk_level=request.risk_level,
            full_response=request.full_response
        )
        
        # Ensure we have bytes
        if not isinstance(pdf_bytes, bytes):
            raise HTTPException(status_code=500, detail="PDF generation returned invalid type")
        
        filename = f"Jal_Rakshak_Report_{request.location.replace(' ', '_')}.pdf"
        
        return Response(
            content=pdf_bytes,
            media_type="application/pdf",
            headers={
                "Content-Disposition": f"attachment; filename={filename}",
                "Content-Type": "application/pdf"
            }
        )
    except HTTPException:
        raise
    except Exception as e:
        import traceback
        error_detail = f"{str(e)}\n{traceback.format_exc()}"
        print(f"Report generation error: {error_detail}")
        raise HTTPException(status_code=500, detail=f"Report generation failed: {str(e)}")
