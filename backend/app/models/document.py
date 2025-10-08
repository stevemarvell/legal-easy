from datetime import datetime, date
from typing import List, Dict, Optional
from pydantic import BaseModel, Field


class Document(BaseModel):
    """Document data model representing a legal document in the system"""
    
    id: str = Field(..., description="Unique identifier for the document", example="doc-001")
    case_id: str = Field(..., description="ID of the case this document belongs to", example="case-001")
    name: str = Field(..., description="Human-readable name of the document", example="Employment Contract - Sarah Chen")
    type: str = Field(..., description="Type of document", example="Contract", enum=["Contract", "Email", "Legal Brief", "Evidence"])
    size: int = Field(..., description="File size in bytes", example=245760)
    upload_date: datetime = Field(..., description="Date when the document was uploaded", example="2024-01-15T09:30:00Z")
    content_preview: str = Field(..., description="Preview of the document content", example="EMPLOYMENT AGREEMENT between TechCorp Solutions Ltd. and Sarah Chen...")
    analysis_completed: bool = Field(..., description="Whether AI analysis has been completed for this document", example=True)

    class Config:
        json_schema_extra = {
            "example": {
                "id": "doc-001",
                "case_id": "case-001",
                "name": "Employment Contract - Sarah Chen",
                "type": "Contract",
                "size": 245760,
                "upload_date": "2024-01-15T09:30:00Z",
                "content_preview": "EMPLOYMENT AGREEMENT between TechCorp Solutions Ltd. and Sarah Chen. Position: Senior Safety Engineer...",
                "analysis_completed": True
            }
        }


class DocumentAnalysis(BaseModel):
    """AI document analysis results containing extracted information and insights"""
    
    document_id: str = Field(..., description="ID of the analyzed document", example="doc-001")
    key_dates: List[date] = Field(..., description="Important dates extracted from the document", example=["2022-03-15", "2024-01-12"])
    parties_involved: List[str] = Field(..., description="Parties mentioned in the document", example=["Sarah Chen", "TechCorp Solutions Inc."])
    document_type: str = Field(..., description="AI-determined document type", example="Employment Contract")
    summary: str = Field(..., description="AI-generated summary of the document", example="At-will employment agreement for Senior Safety Engineer position...")
    key_clauses: List[str] = Field(..., description="Important clauses or sections identified", example=["At-will employment clause", "Safety reporting obligations"])
    confidence_scores: Dict[str, float] = Field(..., description="Confidence scores for different analysis aspects", example={"parties": 0.95, "dates": 0.98})

    class Config:
        json_schema_extra = {
            "example": {
                "document_id": "doc-001",
                "key_dates": ["2022-03-15", "2024-01-12"],
                "parties_involved": ["Sarah Chen", "TechCorp Solutions Inc.", "Marcus Rodriguez"],
                "document_type": "Employment Contract",
                "summary": "At-will employment agreement for Senior Safety Engineer position with 30-day notice provision and standard benefits package.",
                "key_clauses": [
                    "At-will employment clause with 30-day notice requirement",
                    "Safety reporting obligations and whistleblower protections",
                    "Annual salary of $95,000 with performance review eligibility"
                ],
                "confidence_scores": {
                    "parties": 0.95,
                    "dates": 0.98,
                    "contract_terms": 0.92,
                    "key_clauses": 0.89
                }
            }
        }


class KeyInformation(BaseModel):
    """Extracted key information from documents for quick reference"""
    
    dates: List[date] = Field(..., description="Important dates found in the document", example=["2024-01-15", "2024-02-01"])
    parties: List[str] = Field(..., description="Parties mentioned in the document", example=["John Doe", "ABC Corp"])
    amounts: List[str] = Field(..., description="Financial amounts mentioned", example=["$50,000", "£25,000"])
    legal_concepts: List[str] = Field(..., description="Legal concepts identified", example=["breach of contract", "negligence"])
    confidence: float = Field(..., description="Overall confidence score for the extraction", example=0.92, ge=0.0, le=1.0)

    class Config:
        json_schema_extra = {
            "example": {
                "dates": ["2024-01-15", "2024-02-01"],
                "parties": ["John Doe", "ABC Corp", "Legal Counsel"],
                "amounts": ["$50,000", "£25,000"],
                "legal_concepts": ["breach of contract", "negligence", "damages"],
                "confidence": 0.92
            }
        }