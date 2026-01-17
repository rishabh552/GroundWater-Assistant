"""
Test PDF generation to ensure reportlab is working correctly
"""
from backend.report_generator import create_pdf

def test_pdf_generation():
    print("🧪 Testing PDF Report Generation...")
    
    try:
        # Test with sample data
        pdf_bytes = create_pdf(
            query="What is the groundwater status in Chennai?",
            location="Chennai",
            risk_level="Critical",
            full_response="""According to the Chennai District Report 2023 (Page 12), 
            the groundwater situation is concerning with extraction at 85.3% and water levels 
            at 12.4 meters below ground. The district is classified as Semi-Critical.
            
            I recommend implementing rainwater harvesting and monitoring water usage carefully."""
        )
        
        # Check if we got bytes
        if not isinstance(pdf_bytes, bytes):
            print(f"❌ ERROR: Expected bytes, got {type(pdf_bytes)}")
            return False
        
        # Check if PDF has content
        if len(pdf_bytes) == 0:
            print("❌ ERROR: PDF is empty")
            return False
        
        # Save test PDF
        test_file = "test_report.pdf"
        with open(test_file, "wb") as f:
            f.write(pdf_bytes)
        
        print(f"✅ SUCCESS: Generated PDF with {len(pdf_bytes)} bytes")
        print(f"✅ Test PDF saved as: {test_file}")
        print(f"✅ PDF Header: {pdf_bytes[:8]}")  # Should start with %PDF
        
        return True
        
    except Exception as e:
        print(f"❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_pdf_generation()
    exit(0 if success else 1)
