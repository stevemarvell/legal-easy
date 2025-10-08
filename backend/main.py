from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import cases, documents, playbooks, legal_research
import random

app = FastAPI(
    title="AI Legal Platform API",
    description="""
    ## AI-Powered Legal Case Management and Document Analysis API

    This API provides comprehensive legal case management capabilities with AI-powered document analysis.
    
    ### Key Features:
    - **Case Management**: Create, retrieve, and manage legal cases
    - **Document Analysis**: AI-powered analysis of legal documents
    - **Statistics & Analytics**: Dashboard statistics and case insights
    - **Legal Research**: AI-assisted legal research capabilities
    - **Playbook Engine**: Automated legal workflow management

    ### Authentication:
    Currently, this API does not require authentication for demo purposes.
    
    ### Rate Limiting:
    No rate limiting is currently implemented.
    
    ### Support:
    For API support, please contact the development team.
    """,
    version="1.0.0",
    contact={
        "name": "AI Legal Platform Team",
        "email": "support@ailegalplatform.com",
    },
    license_info={
        "name": "MIT License",
        "url": "https://opensource.org/licenses/MIT",
    },
    servers=[
        {
            "url": "http://localhost:8000",
            "description": "Development server"
        },
        {
            "url": "https://api.ailegalplatform.com",
            "description": "Production server"
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

@app.get("/health")
def health_check():
    """Health check endpoint for monitoring and deployment."""
    return {"status": "healthy", "service": "AI Legal Platform API"}

@app.get("/")
def root():
    return {
        "message": "AI Legal Platform API",
        "version": "1.0.0",
        "endpoints": {
            "cases": "/cases",
            "documents": "/documents", 
            "playbooks": "/playbooks",
            "legal_research": "/legal-research",
            "health": "/health"
        }
    }
