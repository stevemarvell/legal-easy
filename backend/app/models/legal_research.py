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
    """Search query for legal research"""
    query: str
    filters: Optional[Dict[str, str]] = None
    limit: int = 10