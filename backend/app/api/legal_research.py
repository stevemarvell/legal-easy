from fastapi import APIRouter
from typing import List
from app.models.legal_research import SearchResult, SearchQuery
from app.services.rag_service import RAGService

router = APIRouter(prefix="/legal-research", tags=["legal-research"])
rag_service = RAGService()


@router.post("/search")
async def search_legal_corpus(query: SearchQuery):
    """Search legal document corpus using RAG with advanced filtering and ranking"""
    results = rag_service.search_legal_corpus(
        query.query, 
        top_k=query.limit,
        min_relevance_score=query.min_relevance_score,
        legal_area=query.legal_area,
        document_type=query.document_type,
        sort_by=query.sort_by,
        content_length_filter=query.content_length_filter,
        include_citations=query.include_citations
    )
    return {"results": results}


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


@router.post("/search/advanced", response_model=List[SearchResult])
async def advanced_search_with_insights(query: SearchQuery):
    """Advanced search with detailed ranking insights and explanations"""
    results = rag_service.search_legal_corpus(
        query.query, 
        top_k=query.limit,
        min_relevance_score=query.min_relevance_score,
        legal_area=query.legal_area,
        document_type=query.document_type,
        sort_by=query.sort_by,
        content_length_filter=query.content_length_filter,
        include_citations=query.include_citations
    )
    
    # Add ranking insights to each result
    for i, result in enumerate(results):
        # Add ranking position and insights as metadata in citation
        ranking_info = f"Rank #{i+1}"
        if result.relevance_score > 0.8:
            ranking_info += " (High Relevance)"
        elif result.relevance_score > 0.6:
            ranking_info += " (Medium Relevance)"
        else:
            ranking_info += " (Lower Relevance)"
        
        result.citation = f"{result.citation} | {ranking_info}"
    
    return results


@router.get("/search/suggestions")
async def get_search_suggestions(query: str):
    """Get search suggestions and query enhancement recommendations"""
    suggestions = []
    query_lower = query.lower()
    
    # Legal term suggestions
    legal_terms = {
        'contract': ['breach of contract', 'contract termination', 'contract formation'],
        'employment': ['wrongful termination', 'employment discrimination', 'workplace harassment'],
        'liability': ['negligence liability', 'product liability', 'professional liability'],
        'intellectual': ['intellectual property', 'copyright infringement', 'trademark violation']
    }
    
    for term, related in legal_terms.items():
        if term in query_lower:
            suggestions.extend([r for r in related if r not in query_lower])
    
    # Add general legal research suggestions if no specific matches
    if not suggestions:
        suggestions = [
            'contract breach remedies',
            'employment law compliance',
            'liability limitations',
            'intellectual property protection'
        ]
    
    return {
        "suggestions": suggestions[:5],
        "query_enhancements": {
            "add_legal_context": f"legal implications of {query}",
            "add_jurisdiction": f"{query} federal law",
            "add_remedies": f"{query} remedies and damages"
        }
    }


@router.get("/filters")
async def get_available_filters():
    """Get available filter options for legal research"""
    return {
        "legal_areas": [
            "Employment Law",
            "Contract Law", 
            "Liability and Risk",
            "Intellectual Property",
            "Corporate Law",
            "Contract Termination",
            "General"
        ],
        "document_types": [
            "Contract Template",
            "Legal Clause",
            "Case Law",
            "Statute/Regulation",
            "Legal Precedent",
            "Contract",
            "Legal Document"
        ],
        "content_length_filters": [
            "short",
            "medium", 
            "long"
        ],
        "sort_options": [
            "relevance",
            "document_type", 
            "legal_area",
            "authority"
        ]
    }