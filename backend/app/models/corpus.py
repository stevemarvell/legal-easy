from typing import List, Optional, Dict, Any
from pydantic import BaseModel
from datetime import datetime


class CorpusItem(BaseModel):
    """Legal corpus item model"""
    id: str
    name: str
    filename: str
    category: str  # contracts, clauses, precedents, statutes
    document_type: str
    research_areas: List[str]
    description: str
    content: Optional[str] = None  # Full content when requested
    research_concepts: Optional[List[str]] = None
    related_items: Optional[List[str]] = None
    relevance_score: Optional[float] = None  # Relevance score for search/related results
    metadata: Optional[Dict[str, Any]] = None


class CorpusCategory(BaseModel):
    """Legal corpus category model"""
    name: str
    description: str
    document_ids: List[str]


class CorpusMetadata(BaseModel):
    """Legal corpus metadata model"""
    version: str
    created_date: str
    total_documents: int
    research_jurisdiction: str
    embedding_model: Optional[str] = None


class ResearchConcept(BaseModel):
    """Research concept model for concept analysis"""
    id: str
    name: str
    definition: str
    related_concepts: List[str]
    corpus_references: List[str]


class CorpusSearchResult(BaseModel):
    """Search result for corpus items"""
    items: List[CorpusItem]
    total_count: int
    query: str
    categories_found: List[str]
    research_areas_found: List[str]


class ConceptAnalysisResult(BaseModel):
    """Result of research concept analysis"""
    concepts: List[ResearchConcept]
    total_concepts: int
    categories_analyzed: List[str]
    research_areas: List[str]