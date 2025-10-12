from datetime import datetime
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field


class DocumentFacts(BaseModel):
    """Facts extracted from a specific document"""
    
    document_name: str = Field(..., description="Name of the document", example="Employment Contract - Sarah Chen")
    key_facts: List[str] = Field(..., description="Key facts extracted from this document", example=["Employment commenced March 15, 2022", "Contract includes anti-retaliation clause"])


class AIAnalysisResult(BaseModel):
    """AI analysis result model for case analysis"""
    
    case_id: str = Field(..., description="ID of the analyzed case", example="case-001")
    timestamp: datetime = Field(..., description="When the analysis was performed", example="2024-01-15T10:00:00Z")
    claim_reference: Optional[str] = Field(None, description="Generated claim reference number", example="CLM-2024-001")
    claimant_name: Optional[str] = Field(None, description="Name of the claimant", example="John Smith")
    incident_date: Optional[str] = Field(None, description="Date of the incident", example="2024-01-10")
    claim_amount: Optional[float] = Field(None, description="Claimed amount if applicable", example=50000.0)
    summary_paragraph_1: Optional[str] = Field(None, description="First summary paragraph of the case analysis")
    summary_paragraph_2: Optional[str] = Field(None, description="Second summary paragraph of the case analysis")
    case_key_facts: List[str] = Field(default_factory=list, description="Key facts extracted from overall case analysis", example=["Employment terminated", "Age discrimination alleged"])
    document_facts: Optional[Dict[str, DocumentFacts]] = Field(default_factory=dict, description="Facts extracted from each document, keyed by document ID")
    confidence: float = Field(..., description="Confidence score of the analysis (0-1)", example=0.85, ge=0, le=1)
    analysis_type: str = Field(default="case_analysis", description="Type of analysis performed", example="case_analysis")
    metadata: Optional[Dict[str, Any]] = Field(default_factory=dict, description="Additional metadata from analysis")

    class Config:
        json_schema_extra = {
            "example": {
                "case_id": "case-001",
                "timestamp": "2024-01-15T10:00:00Z",
                "claim_reference": None,
                "claimant_name": "Sarah Chen",
                "incident_date": "2024-01-12",
                "claim_amount": None,
                "summary_paragraph_1": "This case involves Sarah Chen, a Senior Safety Engineer who was terminated approximately 33 days after submitting a safety violation report...",
                "summary_paragraph_2": "The temporal proximity between her safety report submission and termination raises significant concerns about potential retaliation...",
                "case_key_facts": [
                    "Sarah Chen employed as Senior Safety Engineer since March 15, 2022",
                    "Discovered critical safety violations in Building C on December 8, 2023",
                    "Terminated exactly 33 days later on January 12, 2024"
                ],
                "document_facts": {
                    "doc-001": {
                        "document_name": "Employment Contract - Sarah Chen",
                        "key_facts": [
                            "Employment commenced March 15, 2022 as Senior Safety Engineer",
                            "Contract includes explicit anti-retaliation clause for safety reporting"
                        ]
                    }
                },
                "confidence": 0.92,
                "analysis_type": "case_analysis",
                "metadata": {
                    "documents_analyzed": 3,
                    "processing_time_seconds": 45.2,
                    "model_version": "claude-3-sonnet"
                }
            }
        }


class AIConversation(BaseModel):
    """AI conversation log entry model"""
    
    id: str = Field(..., description="Unique conversation ID", example="conv-001")
    timestamp: datetime = Field(..., description="When the conversation occurred", example="2024-01-15T10:00:00Z")
    analysis_type: str = Field(..., description="Type of analysis performed", example="case_analysis")
    prompt: str = Field(..., description="The prompt sent to AI", example="Analyze the following case documents...")
    response: str = Field(..., description="The AI response received", example="Based on the documents, I found...")
    metadata: Optional[Dict[str, Any]] = Field(default_factory=dict, description="Additional conversation metadata")

    class Config:
        json_schema_extra = {
            "example": {
                "id": "conv-001",
                "timestamp": "2024-01-15T10:00:00Z",
                "analysis_type": "case_analysis",
                "prompt": "Analyze the following case documents for key facts and legal issues...",
                "response": "Based on the documents provided, I have identified the following key facts...",
                "metadata": {
                    "documents_analyzed": ["doc-001", "doc-002"],
                    "processing_time": 45.2,
                    "api_version": "claude-3",
                    "token_usage": {
                        "input_tokens": 1500,
                        "output_tokens": 800
                    }
                }
            }
        }


class AIAnalysisResponse(BaseModel):
    """Response model for AI analysis trigger endpoint"""
    
    success: bool = Field(..., description="Whether the analysis was successful", example=True)
    message: str = Field(..., description="Response message", example="AI analysis completed successfully")
    case_id: str = Field(..., description="ID of the analyzed case", example="case-001")
    analysis: AIAnalysisResult = Field(..., description="The analysis results")

    class Config:
        json_schema_extra = {
            "example": {
                "success": True,
                "message": "AI analysis completed successfully",
                "case_id": "case-001",
                "analysis": {
                    "case_id": "case-001",
                    "timestamp": "2024-01-15T10:00:00Z",
                    "claim_reference": "CLM-2024-001",
                    "claimant_name": "John Smith",
                    "key_facts": ["Employment terminated", "Age discrimination alleged"],
                    "confidence": 0.85,
                    "analysis_type": "case_analysis"
                }
            }
        }


class AIAnalysisGetResponse(BaseModel):
    """Response model for getting AI analysis results"""
    
    success: bool = Field(..., description="Whether the request was successful", example=True)
    case_id: str = Field(..., description="ID of the case", example="case-001")
    analysis: AIAnalysisResult = Field(..., description="The analysis results")

    class Config:
        json_schema_extra = {
            "example": {
                "success": True,
                "case_id": "case-001",
                "analysis": {
                    "case_id": "case-001",
                    "timestamp": "2024-01-15T10:00:00Z",
                    "claim_reference": "CLM-2024-001",
                    "claimant_name": "John Smith",
                    "key_facts": ["Employment terminated", "Age discrimination alleged"],
                    "confidence": 0.85,
                    "analysis_type": "case_analysis"
                }
            }
        }


class AIConversationsResponse(BaseModel):
    """Response model for getting AI conversation log"""
    
    success: bool = Field(..., description="Whether the request was successful", example=True)
    case_id: str = Field(..., description="ID of the case", example="case-001")
    conversations: List[AIConversation] = Field(..., description="List of AI conversations for the case")
    total_conversations: int = Field(..., description="Total number of conversations", example=2)

    class Config:
        json_schema_extra = {
            "example": {
                "success": True,
                "case_id": "case-001",
                "conversations": [
                    {
                        "id": "conv-001",
                        "timestamp": "2024-01-15T10:00:00Z",
                        "analysis_type": "case_analysis",
                        "prompt": "Analyze the following case documents...",
                        "response": "Based on the documents, I found...",
                        "metadata": {
                            "documents_analyzed": ["doc-001", "doc-002"],
                            "processing_time": 45.2,
                            "api_version": "claude-3"
                        }
                    }
                ],
                "total_conversations": 1
            }
        }


class ErrorResponse(BaseModel):
    """Standard error response model"""
    
    detail: str = Field(..., description="Error message", example="Case case-001 not found")

    class Config:
        json_schema_extra = {
            "example": {
                "detail": "Case case-001 not found"
            }
        }