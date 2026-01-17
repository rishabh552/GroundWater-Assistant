"""
Chat endpoint for Jal-Rakshak API
Handles user queries and returns agent responses
"""
import sys
import os

# Add parent directory to path for backend imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
import json

from backend.retriever import GroundwaterRetriever
from backend.llm import load_model
from backend.agent import Agency
from backend.translator import translate_to_english, translate_response

router = APIRouter()

# Global instances (loaded once)
_retriever = None
_llm = None

def get_retriever():
    global _retriever
    if _retriever is None:
        _retriever = GroundwaterRetriever()
        _retriever.load()
    return _retriever

def get_llm():
    global _llm
    if _llm is None:
        _llm = load_model()
    return _llm

class ChatRequest(BaseModel):
    query: str
    language: Optional[str] = None

class ChatResponse(BaseModel):
    response: str
    detected_language: str
    risk_level: str
    query_english: str

@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    Process a user query and return agent response.
    Handles translation if query is not in English.
    """
    try:
        query = request.query.strip()
        if not query:
            raise HTTPException(status_code=400, detail="Query cannot be empty")
        
        # Translate to English if needed
        english_query, detected_lang = translate_to_english(query)
        
        # Get retriever and check if query has results
        retriever = get_retriever()
        results = retriever.search(english_query)
        
        if not results:
            no_data_msg = "No relevant data found for this query. Try a different location name."
            if detected_lang != 'en':
                no_data_msg = translate_response(no_data_msg, detected_lang)
            return ChatResponse(
                response=no_data_msg,
                detected_language=detected_lang,
                risk_level="Unknown",
                query_english=english_query
            )
        
        # Run agent
        llm = get_llm()
        agent = Agency(llm, retriever)
        
        final_response = ""
        for step in agent.run(english_query):
            if step["status"] == "final":
                final_response = step["content"]
                break
        
        # Translate response back if needed
        if detected_lang != 'en' and final_response:
            final_response = translate_response(final_response, detected_lang)
        
        # Extract risk level from response
        risk_level = "Unknown"
        response_lower = final_response.lower()
        if "over-exploited" in response_lower or "overexploited" in response_lower:
            risk_level = "Over-Exploited"
        elif "semi-critical" in response_lower:
            risk_level = "Semi-Critical"
        elif "critical" in response_lower:
            risk_level = "Critical"
        elif "safe" in response_lower:
            risk_level = "Safe"
        
        return ChatResponse(
            response=final_response,
            detected_language=detected_lang,
            risk_level=risk_level,
            query_english=english_query
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/districts")
async def get_districts():
    """Return list of districts with risk levels for map."""
    try:
        with open("generated_map_data.json", "r") as f:
            data = json.load(f)
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
