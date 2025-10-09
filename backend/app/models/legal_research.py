from typing import List, Optional, Dict
from pydantic import BaseModel


class SearchResult(BaseModel):
    """Legal research search result"""
    content: str
    source_document: str
    relevance_score: float
    document_type: str
    citation: str


class LegalClause(BaseModel):
    """Legal clause from document corpus"""
    id: str
    content: str
    source_document: str
    legal_area: str
    clause_type: str
    relevance_score: Optional[float] = None


class SearchQuery(BaseModel):
    """Search query for legal research with enhanced filtering"""
    query: str
    filters: Optional[Dict[str, str]] = None
    limit: int = 10
    min_relevance_score: float = 0.0
    legal_area: Optional[str] = None
    document_type: Optional[str] = None
    content_length_filter: Optional[str] = None  # "short", "medium", "long"
    sort_by: str = "relevance"  # "relevance", "document_type", "legal_area", "authority"
    include_citations: bool = True