from fastapi import APIRouter
from typing import List
from app.models.legal_research import SearchResult, SearchQuery
from app.services.rag_service import RAGService

router = APIRouter(prefix="/legal-research", tags=["legal-research"])
rag_service = RAGService()


@router.post("/search", response_model=List[SearchResult])
async def search_legal_corpus(query: SearchQuery):
    """Search legal document corpus using RAG"""
    # Implementation will be added in later tasks
    pass