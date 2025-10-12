from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import cases, documents, playbooks, corpus
import random
from dotenv import load_dotenv

# Load environment variables from .env file
from pathlib import Path
backend_dir = Path(__file__).parent
env_path = backend_dir / '.env'
load_dotenv(env_path)

app = FastAPI(
    title="Shift Legal AI API",
    description="""
    ## Shift Legal AI - Legal Case Management and Research API

    This API provides legal case management capabilities with AI-powered document analysis and research.
    
    ### Key Features:
    - **Case Management**: Create, retrieve, and manage legal cases
    - **Document Analysis**: AI-powered analysis of legal documents
    - **Statistics & Analytics**: Dashboard statistics and case insights
    - **Playbook Engine**: Automated legal workflow management

    ### Demo Environment:
    This is a demonstration API with sample legal case data.
    
    ### Support:
    For API support, please contact the development team.
    """,
    version="1.0.0",
    contact={
        "name": "Shift Legal AI Team",
        "email": "support@shiftlegalai.com",
    },
    license_info={
        "name": "MIT License",
        "url": "https://opensource.org/licenses/MIT",
    },
    servers=[
        {
            "url": "http://localhost:8000",
            "description": "Development server"
        }
    ]
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

# Include API routers with /api prefix
app.include_router(cases.router, prefix="/api")
app.include_router(documents.router, prefix="/api")
app.include_router(playbooks.router, prefix="/api")
app.include_router(corpus.router, prefix="/api")


# Legacy endpoint for backward compatibility
@app.get("/random")
def get_random():
    """Return a random integer between 0 and 100 inclusive."""
    return {"value": random.randint(0, 100)}

@app.get("/health")
def health_check():
    """Health check endpoint for monitoring and deployment."""
    return {"status": "healthy", "service": "Shift Legal AI API"}

@app.get("/")
def root():
    return {
        "message": "Shift Legal AI Platform API",
        "version": "1.0.0",
        "endpoints": {
            "cases": "/api/cases",
            "documents": "/api/documents", 
            "playbooks": "/api/playbooks",
            "corpus": "/api/corpus",

            "health": "/health"
        }
    }
