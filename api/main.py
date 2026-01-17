"""
FastAPI Backend for Jal-Rakshak
Provides chat and report endpoints

Run with: uvicorn api.main:app --reload --port 8000
(from the jal-rakshak root directory)
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routes import chat, report, map

app = FastAPI(
    title="Jal-Rakshak API",
    description="Groundwater Advisory System API",
    version="1.0.0"
)

# CORS for Next.js frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(chat.router, prefix="/api", tags=["Chat"])
app.include_router(report.router, prefix="/api", tags=["Report"])
app.include_router(map.router, prefix="/api", tags=["Map"])

@app.get("/")
async def root():
    return {"message": "Jal-Rakshak API", "status": "running"}

@app.get("/health")
async def health():
    return {"status": "healthy"}
