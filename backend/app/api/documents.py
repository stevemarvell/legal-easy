from fastapi import APIRouter, HTTPException, Path
from typing import List
from app.models.document import Document
from app.services.documents_service import DocumentsService


router = APIRouter(
    prefix="/documents", 
    tags=["Documents"],
    responses={
        404: {"description": "Document not found"},
        500: {"description": "Internal server error"}
    }
)


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
                            "content_preview": "EMPLOYMENT AGREEMENT between TechCorp Solutions Ltd. and Sarah Chen..."
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
        documents = DocumentsService.load_case_documents(case_id)
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
                        "content_preview": "EMPLOYMENT AGREEMENT between TechCorp Solutions Ltd. and Sarah Chen..."
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
        # Find the document using DocumentsService
        document = DocumentsService.find_document_by_id(document_id)
        if document:
            return document
        
        raise HTTPException(status_code=404, detail=f"Document with ID {document_id} not found")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get document: {str(e)}")


@router.get(
    "/{document_id}/content",
    summary="Get full document content",
    description="""
    Retrieve the complete text content of a specific document.
    
    This endpoint returns the full document text content for viewing purposes.
    Useful for:
    - Document review and reading
    - Content verification
    """,
    responses={
        200: {
            "description": "Document content retrieved successfully",
            "content": {
                "application/json": {
                    "example": {
                        "document_id": "doc-001",
                        "content": "EMPLOYMENT AGREEMENT\n\nThis Employment Agreement (\"Agreement\") is entered into on 15 March 2022...",
                        "content_length": 2456
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
        },
        500: {
            "description": "Failed to retrieve content",
            "content": {
                "application/json": {
                    "example": {"detail": "Failed to read document content: File not accessible"}
                }
            }
        }
    }
)
async def get_document_content(
    document_id: str = Path(..., description="Unique identifier of the document", example="doc-001")
):
    """Get the full text content of a specific document"""
    try:
        # Load document content using DocumentsService
        content = DocumentsService.load_document_content(document_id)
        if not content:
            raise HTTPException(status_code=404, detail=f"Document with ID {document_id} not found")
        
        return {
            "document_id": document_id,
            "content": content,
            "content_length": len(content)
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve document content: {str(e)}")

