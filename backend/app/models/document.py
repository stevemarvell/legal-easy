from datetime import datetime, date
from typing import List, Dict, Optional
from pydantic import BaseModel


class Document(BaseModel):
    """Document data model"""
    id: str
    case_id: str
    name: str
    type: str  # "Contract", "Email", "Legal Brief", "Evidence"
    size: int
    upload_date: datetime
    content_preview: str
    analysis_completed: bool


class DocumentAnalysis(BaseModel):
    """AI document analysis results"""
    document_id: str
    key_dates: List[date]
    parties_involved: List[str]
    document_type: str
    summary: str
    key_clauses: List[str]
    confidence_scores: Dict[str, float]


class KeyInformation(BaseModel):
    """Extracted key information from documents"""
    dates: List[date]
    parties: List[str]
    amounts: List[str]
    legal_concepts: List[str]
    confidence: float