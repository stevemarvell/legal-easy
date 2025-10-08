from fastapi import APIRouter
from typing import List
from app.models.legal_research import SearchResult, SearchQuery
from app.services.rag_service import RAGService

router = APIRouter(prefix="/legal-research", tags=["legal-research"])
rag_service = RAGService()


@router.post("/search", response_model=List[SearchResult])
async def search_legal_corpus(query: SearchQuery):
    """Search legal document corpus using RAG with advanced filtering and ranking"""
    results = rag_service.search_legal_corpus(
        query.query, 
        top_k=query.limit,
        min_relevance_score=query.min_relevance_score,
        legal_area=query.legal_area,
        document_type=query.document_type,
        sort_by=query.sort_by
    )
    return results


@router.get("/categories")
async def get_document_categories():
    """Get available document categories"""
    return {
        "categories": rag_service.get_document_categories(),
        "statistics": rag_service.get_corpus_statistics()
    }


@router.post("/search/{category}", response_model=List[SearchResult])
async def search_by_category(category: str, query: SearchQuery):
    """Search within specific legal category"""
    results = rag_service.search_by_category(
        query.query, 
        category, 
        top_k=query.limit
    )
    return results


@router.get("/clauses")
async def get_relevant_clauses(context: str, legal_area: str = None):
    """Get relevant legal clauses for given context"""
    clauses = rag_service.get_relevant_clauses(context, legal_area)
    return {"clauses": clauses}


@router.get("/corpus/stats")
async def get_corpus_statistics():
    """Get statistics about the legal corpus"""
    return rag_service.get_corpus_statistics()


@router.get("/filters")
async def get_available_filters():
    """Get available filter options for legal research"""
    return {
        "legal_areas": [
            "Employment Law",
            "Contract Law", 
            "Liability and Risk",
            "Intellectual Property",
            "Contract Termination",
            "General"
        ],
        "document_types": [
            "Contract Template",
            "Legal Clause",
            "Case Law",
            "Statute/Regulation"
        ],
        "sort_options": [
            "relevance",
            "document_type", 
            "legal_area"
        ]
    }