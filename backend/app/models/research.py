from typing import List, Optional, Dict
from pydantic import BaseModel


class SearchResult(BaseModel):
    """Research search result for granular content"""
    content: str
    source_document: str
    relevance_score: float
    document_type: str
    citation: str
    research_area: Optional[str] = None
    content_type: Optional[str] = None  # "clause", "section", "paragraph", etc.


class ResearchClause(BaseModel):
    """Research clause or section from document corpus"""
    id: str
    content: str
    source_document: str
    research_area: str
    clause_type: str
    relevance_score: Optional[float] = None
    category: Optional[str] = None  # contracts, clauses, precedents, statutes


class SearchQuery(BaseModel):
    """Search query for research with enhanced filtering"""
    query: str
    filters: Optional[Dict[str, str]] = None
    limit: int = 10
    min_relevance_score: float = 0.0
    research_area: Optional[str] = None
    document_type: Optional[str] = None
    category: Optional[str] = None  # contracts, clauses, precedents, statutes
    content_length_filter: Optional[str] = None  # "short", "medium", "long"
    sort_by: str = "relevance"  # "relevance", "document_type", "research_area", "authority"
    include_citations: bool = True


class ResearchFilter(BaseModel):
    """Filter options for research queries"""
    research_areas: Optional[List[str]] = None
    document_types: Optional[List[str]] = None
    categories: Optional[List[str]] = None
    date_range: Optional[Dict[str, str]] = None
    content_length: Optional[str] = None
    authority_level: Optional[str] = None


class ResearchSummary(BaseModel):
    """Summary of research results"""
    total_results: int
    research_areas_found: List[str]
    document_types_found: List[str]
    categories_found: List[str]
    top_relevance_score: float
    query_processed: str


class DetailedSearchResult(BaseModel):
    """Comprehensive search result with context"""
    results: List[SearchResult]
    summary: ResearchSummary
    related_concepts: List[str]
    suggested_queries: List[str]
    filters_applied: Optional[ResearchFilter] = None


class ResearchContext(BaseModel):
    """Context for research queries"""
    user_intent: Optional[str] = None  # "find_template", "analyze_precedent", "compare_clauses"
    case_context: Optional[str] = None
    jurisdiction: Optional[str] = None
    practice_area: Optional[str] = None