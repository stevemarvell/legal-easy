from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import cases, documents, playbooks, legal_research
import random

app = FastAPI(
    title="AI Legal Platform API",
    description="API for AI-powered legal case management and document analysis",
    version="1.0.0"
)

# CORS: allow frontend origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",  # Vite dev server
        "http://localhost:8080", 
        "http://127.0.0.1:8080",
        "https://legal-easy-frontend-production.up.railway.app", 
    ],
    allow_credentials=False,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"]
)

# Include API routers
app.include_router(cases.router)
app.include_router(documents.router)
app.include_router(playbooks.router)
app.include_router(legal_research.router)

# Legacy endpoint for backward compatibility
@app.get("/random")
def get_random():
    """Return a random integer between 0 and 100 inclusive."""
    return {"value": random.randint(0, 100)}

@app.get("/")
def root():
    return {
        "message": "AI Legal Platform API",
        "version": "1.0.0",
        "endpoints": {
            "cases": "/cases",
            "documents": "/documents", 
            "playbooks": "/playbooks",
            "legal_research": "/legal-research"
        }
    }
