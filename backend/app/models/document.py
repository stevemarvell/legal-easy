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

    full_content_path: Optional[str] = Field(None, description="Path to the full document content file", example="backend/data/case_documents/case-001/doc-001_employment_contract_sarah_chen.txt")

    class Config:
        json_schema_extra = {
            "example": {
                "id": "doc-001",
                "case_id": "case-001",
                "name": "Employment Contract - Sarah Chen",
                "type": "Contract",
                "size": 245760,
                "upload_date": "2024-01-15T09:30:00Z",
                "content_preview": "EMPLOYMENT AGREEMENT between TechCorp Solutions Ltd. and Sarah Chen. Position: Senior Safety Engineer..."
            }
        }


