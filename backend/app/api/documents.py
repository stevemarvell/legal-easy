from fastapi import APIRouter, HTTPException, Path
from typing import List
from app.models.document import Document, DocumentAnalysis
from app.services.document_service import DocumentService

router = APIRouter(
    prefix="/documents", 
    tags=["Documents"],
    responses={
        404: {"description": "Document or analysis not found"},
        500: {"description": "Internal server error"}
    }
)
document_service = DocumentService()


@router.get(
    "/cases/{case_id}/documents", 
    response_model=List[Document],
    summary="Get documents for a case",
    description="""
    Retrieve all documents associated with a specific legal case.
    
    This endpoint returns a list of all documents that belong to the specified case,
    including:
    - Document metadata (name, type, size, upload date)
    - Content preview
    - Analysis completion status
    
    **Use cases:**
    - Case document listing
    - Document management interfaces
    - Bulk document operations
    """,
    responses={
        200: {
            "description": "Documents retrieved successfully",
            "content": {
                "application/json": {
                    "example": [
                        {
                            "id": "doc-001",
                            "case_id": "case-001",
                            "name": "Employment Contract - Sarah Chen",
                            "type": "Contract",
                            "size": 245760,
                            "upload_date": "2024-01-15T09:30:00Z",
                            "content_preview": "EMPLOYMENT AGREEMENT between TechCorp Solutions Ltd. and Sarah Chen...",
                            "analysis_completed": True
                        }
                    ]
                }
            }
        }
    }
)
async def get_case_documents(
    case_id: str = Path(..., description="Unique identifier of the case", example="case-001")
):
    """Get all documents associated with a specific legal case"""
    try:
        documents = document_service.get_case_documents(case_id)
        return documents
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get case documents: {str(e)}")


@router.get(
    "/{document_id}", 
    response_model=Document,
    summary="Get document by ID",
    description="""
    Retrieve detailed information about a specific document.
    
    This endpoint returns complete document information including:
    - Document metadata and properties
    - Content preview
    - Analysis status
    - Associated case information
    
    **Use cases:**
    - Document detail views
    - Document management operations
    - Pre-analysis document inspection
    """,
    responses={
        200: {
            "description": "Document retrieved successfully",
            "content": {
                "application/json": {
                    "example": {
                        "id": "doc-001",
                        "case_id": "case-001",
                        "name": "Employment Contract - Sarah Chen",
                        "type": "Contract",
                        "size": 245760,
                        "upload_date": "2024-01-15T09:30:00Z",
                        "content_preview": "EMPLOYMENT AGREEMENT between TechCorp Solutions Ltd. and Sarah Chen...",
                        "analysis_completed": True
                    }
                }
            }
        },
        404: {
            "description": "Document not found",
            "content": {
                "application/json": {
                    "example": {"detail": "Document with ID doc-999 not found"}
                }
            }
        }
    }
)
async def get_document(
    document_id: str = Path(..., description="Unique identifier of the document", example="doc-001")
):
    """Get detailed information about a specific document"""
    try:
        document = document_service.get_document_by_id(document_id)
        if document is None:
            raise HTTPException(status_code=404, detail=f"Document with ID {document_id} not found")
        return document
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get document: {str(e)}")


@router.get(
    "/{document_id}/analysis", 
    response_model=DocumentAnalysis,
    summary="Get AI analysis for document",
    description="""
    Retrieve AI-powered analysis results for a specific document.
    
    This endpoint returns comprehensive AI analysis including:
    - Extracted key dates and parties
    - Document type classification
    - AI-generated summary
    - Important clauses and legal concepts
    - Confidence scores for analysis accuracy
    
    **Use cases:**
    - Document analysis views
    - Legal research and discovery
    - Case preparation and strategy
    - Automated document processing
    """,
    responses={
        200: {
            "description": "Document analysis retrieved successfully",
            "content": {
                "application/json": {
                    "example": {
                        "document_id": "doc-001",
                        "key_dates": ["2022-03-15", "2024-01-12"],
                        "parties_involved": ["Sarah Chen", "TechCorp Solutions Inc."],
                        "document_type": "Employment Contract",
                        "summary": "At-will employment agreement for Senior Safety Engineer position...",
                        "key_clauses": ["At-will employment clause", "Safety reporting obligations"],
                        "confidence_scores": {"parties": 0.95, "dates": 0.98}
                    }
                }
            }
        },
        404: {
            "description": "Document analysis not found",
            "content": {
                "application/json": {
                    "example": {"detail": "Analysis for document doc-999 not found"}
                }
            }
        }
    }
)
async def get_document_analysis(
    document_id: str = Path(..., description="Unique identifier of the document to analyze", example="doc-001")
):
    """Get AI-powered analysis results for a specific document"""
    try:
        analysis = document_service.get_document_analysis(document_id)
        if analysis is None:
            raise HTTPException(status_code=404, detail=f"Analysis for document {document_id} not found")
        return analysis
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get document analysis: {str(e)}")