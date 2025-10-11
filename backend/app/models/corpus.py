from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field
from datetime import datetime


class CorpusItem(BaseModel):
    """Legal corpus item model as specified in design document"""
    id: str
    title: str
    category: str  # contracts, clauses, precedents, statutes
    content: Optional[str] = None  # Optional for browsing, required for full item view
    legal_concepts: List[str] = []
    related_items: List[str] = []
    metadata: Dict[str, Any] = {}
    
    # Additional fields from the data structure
    filename: Optional[str] = None
    document_type: Optional[str] = None
    research_areas: List[str] = []
    description: Optional[str] = None


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


class LegalConcept(BaseModel):
    """Legal concept model as specified in design document"""
    id: str
    name: str
    definition: str
    related_concepts: List[str]
    corpus_references: List[str]


class ResearchConcept(BaseModel):
    """Research concept model for concept analysis (legacy compatibility)"""
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