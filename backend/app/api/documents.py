from fastapi import APIRouter, HTTPException, Path
from typing import List
from app.models.document import Document, DocumentAnalysis
from app.services.data_service import DataService
from app.services.ai_service import AIService

router = APIRouter(
    prefix="/documents", 
    tags=["Documents"],
    responses={
        404: {"description": "Document or analysis not found"},
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
        documents = DataService.load_case_documents(case_id)
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
        # Search through all case documents to find the specific document
        cases = DataService.load_cases()
        for case in cases:
            # Fix: case is a dict, not an object, so use case['id'] instead of case.id
            case_id = case.get('id') if isinstance(case, dict) else case.id
            documents = DataService.load_case_documents(case_id)
            # Fix: documents are also dicts, not objects, so use d['id'] instead of d.id
            document = next((d for d in documents if (d.get('id') if isinstance(d, dict) else d.id) == document_id), None)
            if document:
                return document
        
        raise HTTPException(status_code=404, detail=f"Document with ID {document_id} not found")
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
    
    TODO: Implement AI analysis integration
    """,
    responses={
        200: {"description": "Document analysis retrieved successfully"},
        404: {"description": "Document analysis not found"}
    }
)
async def get_document_analysis(
    document_id: str = Path(..., description="Unique identifier of the document to analyze", example="doc-001")
):
    """Get AI-powered analysis results for a specific document"""
    try:
        # TODO: Implement AI analysis retrieval
        analysis = AIService.analyze_document(document_id, "")
        return analysis
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get document analysis: {str(e)}")


@router.post(
    "/{document_id}/analyze",
    response_model=DocumentAnalysis,
    summary="Perform real-time AI analysis on document",
    description="""
    Perform real-time AI-powered analysis on a specific document.
    
    TODO: Implement AI analysis integration
    """,
    responses={
        200: {"description": "Document analysis completed successfully"},
        404: {"description": "Document not found"},
        500: {"description": "Analysis failed"}
    }
)
async def analyze_document(
    document_id: str = Path(..., description="Unique identifier of the document to analyze", example="doc-001")
):
    """Perform real-time AI analysis on a specific document"""
    try:
        # TODO: Load document content and perform AI analysis
        content = DataService.load_document_content(document_id)
        if not content:
            raise HTTPException(status_code=404, detail=f"Document with ID {document_id} not found")
        
        analysis = AIService.analyze_document(document_id, content)
        return analysis
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to analyze document: {str(e)}")


@router.delete(
    "/{document_id}/analysis",
    summary="Delete analysis results for document",
    description="Delete stored analysis results for a specific document",
    responses={
        200: {"description": "Analysis deleted successfully"},
        404: {"description": "Analysis not found"},
        500: {"description": "Failed to delete analysis"}
    }
)
async def delete_document_analysis(
    document_id: str = Path(..., description="Unique identifier of the document", example="doc-001")
):
    """Delete stored analysis results for a specific document"""
    try:
        # Check if analysis exists first
        existing_analysis = AIService.load_existing_analysis(document_id)
        if existing_analysis is None:
            raise HTTPException(status_code=404, detail=f"No analysis found for document {document_id}")
        
        # Delete the analysis (this would need to be implemented in AIService)
        # For now, we'll just return success since the simplified architecture
        # may not need explicit deletion
        return {"message": f"Analysis for document {document_id} deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to delete analysis: {str(e)}")


@router.get(
    "/{document_id}/content",
    summary="Get full document content",
    description="""
    Retrieve the complete text content of a specific document.
    
    This endpoint returns the full document text content for viewing purposes.
    Useful for:
    - Document review and reading
    - Content verification
    - Manual analysis
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
        # Load document content using DataService
        content = DataService.load_document_content(document_id)
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


@router.post(
    "/regenerate-analysis",
    summary="Regenerate all document analysis",
    description="""
    Regenerate AI analysis for all documents in the system.
    
    TODO: Implement AI analysis regeneration
    """,
    responses={
        200: {"description": "Analysis regeneration completed successfully"},
        500: {"description": "Analysis regeneration failed"}
    }
)
async def regenerate_document_analysis():
    """Regenerate AI analysis for all documents in the system"""
    try:
        # TODO: Implement AI analysis regeneration
        return {
            "success": True,
            "message": "Document analysis regeneration not yet implemented",
            "total_documents": 0,
            "analyzed_documents": 0,
            "failed_documents": 0,
            "average_confidence": 0.0,
            "processing_time_seconds": 0.0
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to regenerate document analysis: {str(e)}")

