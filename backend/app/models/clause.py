#!/usr/bin/env python3
"""
Clause models for the Legal AI System

This module contains Pydantic models for clause extraction and management.
"""

from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field
from datetime import datetime
from enum import Enum


class ClauseType(str, Enum):
    """Types of clauses that can be extracted."""
    NUMBERED = "numbered"
    TITLED = "titled"
    PARAGRAPH = "paragraph"
    SECTION = "section"
    SUBSECTION = "subsection"


class ExtractionMethod(str, Enum):
    """Methods used for clause extraction."""
    NUMBERED_LIST_PARSER = "numbered_list_parser"
    SECTION_HEADER_PARSER = "section_header_parser"
    LEGAL_SECTION_PARSER = "legal_section_parser"
    AI_TEXT_ANALYSIS = "ai_text_analysis"
    PARAGRAPH_SPLITTER = "paragraph_splitter"


class ProcessingStatus(str, Enum):
    """Processing status for clause extraction."""
    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    SKIPPED = "skipped"


class ClauseBoundary(BaseModel):
    """Model for clause boundary detection."""
    start_position: int = Field(..., description="Start character position in document")
    end_position: int = Field(..., description="End character position in document")
    title: str = Field(..., description="Title or identifier of the clause")
    clause_type: ClauseType = Field(..., description="Type of clause boundary")
    confidence_score: float = Field(default=1.0, ge=0.0, le=1.0, description="Confidence in boundary detection")


class ExtractedClause(BaseModel):
    """Model for extracted clause data."""
    id: str = Field(..., description="Unique clause ID in format {source_document_id}_clause_{number}")
    title: str = Field(..., description="Title or heading of the clause")
    content: str = Field(..., description="Full content of the clause")
    source_document_id: str = Field(..., description="ID of the source document")
    source_document_title: str = Field(..., description="Title of the source document")
    category: str = Field(..., description="Category inherited from source document")
    clause_number: int = Field(..., description="Sequential number within the document")
    legal_concepts: List[str] = Field(default_factory=list, description="Legal concepts identified in the clause")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata")

    def __init__(self, **data):
        super().__init__(**data)
        # Ensure metadata has required fields
        if 'extraction_timestamp' not in self.metadata:
            self.metadata['extraction_timestamp'] = datetime.now().isoformat()
        if 'extraction_method' not in self.metadata:
            self.metadata['extraction_method'] = ExtractionMethod.PARAGRAPH_SPLITTER
        if 'confidence_score' not in self.metadata:
            self.metadata['confidence_score'] = 1.0
        if 'formatting_preserved' not in self.metadata:
            self.metadata['formatting_preserved'] = True


class ClauseContent(BaseModel):
    """Model for extracted clause content."""
    title: str = Field(..., description="Title of the clause")
    content: str = Field(..., description="Content of the clause")
    formatting_preserved: bool = Field(default=True, description="Whether original formatting was preserved")
    legal_concepts: List[str] = Field(default_factory=list, description="Identified legal concepts")


class ProcessingResult(BaseModel):
    """Result of clause processing operation."""
    document_id: str = Field(..., description="ID of the processed document")
    status: ProcessingStatus = Field(..., description="Processing status")
    clauses_extracted: int = Field(default=0, description="Number of clauses extracted")
    processing_time_seconds: float = Field(default=0.0, description="Time taken for processing")
    error_message: Optional[str] = Field(default=None, description="Error message if processing failed")
    extraction_method: ExtractionMethod = Field(..., description="Method used for extraction")


class ExtractionMetrics(BaseModel):
    """Metrics for clause extraction performance."""
    document_id: str = Field(..., description="ID of the processed document")
    total_characters: int = Field(..., description="Total characters in document")
    clauses_found: int = Field(..., description="Number of clauses found")
    boundaries_detected: int = Field(..., description="Number of boundaries detected")
    average_confidence: float = Field(..., description="Average confidence score")
    processing_time: float = Field(..., description="Processing time in seconds")
    extraction_method: ExtractionMethod = Field(..., description="Method used for extraction")


# Additional models for frontend compatibility
class ClauseCategory(str, Enum):
    """Categories for clause classification."""
    POLICY = "policy"
    REGULATION = "regulation"
    PRECEDENT = "precedent"
    GUIDELINE = "guideline"


class Clause(BaseModel):
    """Simplified clause model for frontend compatibility."""
    id: str = Field(..., description="Unique clause identifier")
    document_source: str = Field(..., description="Source document identifier")
    clause_number: str = Field(..., description="Clause number within document")
    category: ClauseCategory = Field(..., description="Clause category")
    title: str = Field(..., description="Clause title")
    content: str = Field(..., description="Clause content")
    tags: List[str] = Field(default_factory=list, description="Associated tags")
    relevance_keywords: List[str] = Field(default_factory=list, description="Keywords for relevance matching")


class ClauseSearchResult(BaseModel):
    """Search result containing clause and relevance score."""
    clause: Clause = Field(..., description="The matched clause")
    relevance_score: float = Field(..., ge=0.0, le=1.0, description="Relevance score between 0 and 1")


# Utility functions for model conversion
def extracted_clause_to_clause(extracted_clause: ExtractedClause) -> Clause:
    """Convert ExtractedClause to simplified Clause model for frontend."""
    # Map categories to frontend categories
    category_mapping = {
        "contracts": ClauseCategory.POLICY,
        "clauses": ClauseCategory.REGULATION,
        "precedents": ClauseCategory.PRECEDENT,
        "statutes": ClauseCategory.GUIDELINE
    }
    
    category = category_mapping.get(extracted_clause.category, ClauseCategory.POLICY)
    
    # Generate enhanced relevance keywords from title and content
    relevance_keywords = _generate_relevance_keywords(
        extracted_clause.title, 
        extracted_clause.content, 
        extracted_clause.legal_concepts
    )
    
    # Extract actual clause number from content if it starts with a number
    actual_clause_number = _extract_actual_clause_number(extracted_clause.content, extracted_clause.title)
    
    return Clause(
        id=extracted_clause.id,
        document_source=extracted_clause.source_document_id,
        clause_number=actual_clause_number,
        category=category,
        title=extracted_clause.title,
        content=extracted_clause.content,
        tags=extracted_clause.legal_concepts,  # Use legal concepts as tags
        relevance_keywords=relevance_keywords
    )


def _extract_actual_clause_number(content: str, title: str) -> str:
    """Extract the actual clause number from content or title."""
    # Check if content starts with a number pattern like "1. TITLE"
    import re
    
    # Look for pattern at start of content
    content_match = re.match(r'^(\d+)\.', content.strip())
    if content_match:
        return content_match.group(1)
    
    # Look for pattern in title (for cases where title contains the number)
    title_match = re.search(r'(\d+)\.', title)
    if title_match:
        return title_match.group(1)
    
    # Check if it's a header/summary clause
    if "DOCUMENT HEADER" in title.upper() or "HEADER" in title.upper():
        return "0"  # Use 0 for header sections
    
    # Fallback to "1" if no number found
    return "1"


def _generate_relevance_keywords(title: str, content: str, legal_concepts: List[str]) -> List[str]:
    """Generate relevance keywords from clause title, content, and legal concepts."""
    keywords = set()
    
    # Add legal concepts
    keywords.update(legal_concepts)
    
    # Extract key terms from title
    title_words = title.lower().replace('-', ' ').replace('_', ' ').split()
    title_keywords = [word for word in title_words if len(word) > 3 and word not in ['document', 'header', 'clause']]
    keywords.update(title_keywords)
    
    # Extract key terms from content (first 200 characters for efficiency)
    content_sample = content[:200].lower()
    
    # Common legal and business terms that are relevant for search
    relevant_terms = {
        'auto', 'vehicle', 'car', 'motor', 'property', 'injury', 'medical', 'hospital', 
        'fracture', 'head', 'health', 'solicitor', 'lawyer', 'attorney', 'legal', 
        'counsel', 'disputed', 'contest', 'investigation', 'witness', 'evidence', 
        'fair', 'prompt', 'guidance', 'reject', 'regulatory', 'large', 'high', 
        'value', 'expensive', 'senior', 'manager', 'approval', 'wet', 'floor', 
        'slip', 'warning', 'signs', 'contributory', 'negligence', 'retail', 
        'professional', 'architect', 'engineer', 'design', 'technical', 'fraud', 
        'suspicious', 'inconsistent', 'false', 'fabricated', 'settle', 'settlement', 
        'authority', 'approve', 'pay', 'payout', 'threshold', 'review', 'escalation',
        'services', 'provider', 'client', 'payment', 'terms', 'performance', 
        'standards', 'intellectual', 'property', 'limitation', 'liability', 
        'indemnification', 'termination', 'dispute', 'resolution', 'force', 
        'majeure', 'entire', 'agreement', 'governing', 'law'
    }
    
    # Find relevant terms in content
    for term in relevant_terms:
        if term in content_sample:
            keywords.add(term)
    
    # Remove empty strings and convert to list
    keywords = [k for k in keywords if k and len(k) > 2]
    
    return sorted(list(set(keywords)))  # Remove duplicates and sort