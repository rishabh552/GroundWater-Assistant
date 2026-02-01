"""
Configuration settings for Jal-Rakshak
"""
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file if present
load_dotenv()

# Base paths - PROJECT_ROOT is parent of backend/
PROJECT_ROOT = Path(__file__).parent.parent
DATA_DIR = PROJECT_ROOT / "data"
PDF_DIR = DATA_DIR / "pdfs"
VECTORSTORE_DIR = PROJECT_ROOT / "vectorstore"
MODELS_DIR = PROJECT_ROOT / "models"

# Create directories if they don't exist
PDF_DIR.mkdir(parents=True, exist_ok=True)
VECTORSTORE_DIR.mkdir(parents=True, exist_ok=True)
MODELS_DIR.mkdir(parents=True, exist_ok=True)

# LLM Settings (using HuggingFace Transformers)
# Model ID can be overridden via environment variable
LLM_MODEL_ID = os.getenv("LLM_MODEL_ID", "ibm-granite/granite-3.0-2b-instruct")
LLM_CONTEXT_LENGTH = 4096
LLM_TEMPERATURE = 0.1  # Low for factual responses
LLM_MAX_TOKENS = 1024  # Increased for Gemini 2.5 verbose reasoning

# LLM Provider Settings
# Options: 'local' (Granite) or 'gemini' (Google API)
LLM_PROVIDER = os.getenv("LLM_PROVIDER", "local").lower()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
GEMINI_MODEL_ID = os.getenv("GEMINI_MODEL_ID", "gemini-2.5-flash")  # Can be overridden via .env (e.g., gemma-3-27b-it)

# Embedding Settings
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200

# Retrieval Settings
TOP_K_RESULTS = 5  # Increased to ensure Officer persona gets sufficient detail

# Risk Classification Mapping
RISK_LEVELS = {
    "safe": {
        "level": "🟢 LOW RISK",
        "advice": "Drilling is generally safe. Monitor water levels post-monsoon."
    },
    "semi-critical": {
        "level": "🟡 MODERATE RISK", 
        "advice": "Proceed with caution. Consider rainwater harvesting as backup."
    },
    "critical": {
        "level": "🟠 HIGH RISK",
        "advice": "High risk of dry borewell. Consult local groundwater office before drilling."
    },
    "over-exploited": {
        "level": "🔴 VERY HIGH RISK - DRILLING NOT ADVISED",
        "advice": "Groundwater extraction exceeds recharge. Alternative water sources recommended."
    }
}

# UI Settings
APP_TITLE = "🌊 Jal-Rakshak: Groundwater Risk Advisor"
APP_SUBTITLE = "Protecting farmers from failed borewells across Tamil Nadu"
