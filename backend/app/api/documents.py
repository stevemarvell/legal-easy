from fastapi import APIRouter, HTTPException, Path
from typing import List
from app.models.document import Document, DocumentAnalysis
from app.services.document_service import DocumentService
from app.services.ai_analysis_service import AIAnalysisService
from app.services.analysis_storage_service import AnalysisStorageService

router = APIRouter(
    prefix="/documents", 
    tags=["Documents"],
    responses={
        404: {"description": "Document or analysis not found"},
        500: {"description": "Internal server error"}
    }
)
document_service = DocumentService()
ai_analysis_service = AIAnalysisService()
analysis_storage_service = AnalysisStorageService()


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
        # Check for live analysis results only
        live_analysis = analysis_storage_service.get_analysis(document_id)
        if live_analysis is not None:
            return live_analysis
        
        # No analysis found
        raise HTTPException(status_code=404, detail=f"Analysis for document {document_id} not found")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get document analysis: {str(e)}")


@router.post(
    "/{document_id}/analyze",
    response_model=DocumentAnalysis,
    summary="Perform real-time AI analysis on document",
    description="""
    Perform real-time AI-powered analysis on a specific document.
    
    This endpoint triggers immediate AI analysis of the document and returns:
    - Extracted key dates and parties
    - Document type classification
    - AI-generated summary
    - Important clauses and legal concepts
    - Confidence scores for analysis accuracy
    
    **Use cases:**
    - Real-time document processing
    - On-demand analysis for new documents
    - Re-analysis of existing documents
    - Testing and validation of AI analysis capabilities
    
    **Note:** This endpoint performs live analysis and may take longer than 
    retrieving pre-computed results from the GET endpoint.
    """,
    responses={
        200: {
            "description": "Document analysis completed successfully",
            "content": {
                "application/json": {
                    "example": {
                        "document_id": "doc-001",
                        "key_dates": ["2022-03-15", "2024-01-12"],
                        "parties_involved": ["Sarah Chen", "TechCorp Solutions Inc."],
                        "document_type": "Employment Contract",
                        "summary": "Real-time analysis of employment agreement for Senior Safety Engineer position...",
                        "key_clauses": ["At-will employment clause", "Safety reporting obligations"],
                        "confidence_scores": {"parties": 0.95, "dates": 0.98}
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
            "description": "Analysis failed",
            "content": {
                "application/json": {
                    "example": {"detail": "Failed to analyze document: AI service unavailable"}
                }
            }
        }
    }
)
async def analyze_document(
    document_id: str = Path(..., description="Unique identifier of the document to analyze", example="doc-001")
):
    """Perform real-time AI analysis on a specific document"""
    try:
        # First, get the document
        document = document_service.get_document_by_id(document_id)
        if document is None:
            raise HTTPException(status_code=404, detail=f"Document with ID {document_id} not found")
        
        # Perform AI analysis
        analysis = ai_analysis_service.analyze_document(document)
        
        # Save the analysis results for future retrieval
        save_success = analysis_storage_service.save_analysis(document_id, analysis)
        if not save_success:
            print(f"Warning: Failed to save analysis results for document {document_id}")
        
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
        success = analysis_storage_service.delete_analysis(document_id)
        if not success:
            raise HTTPException(status_code=404, detail=f"No analysis found for document {document_id}")
        
        return {"message": f"Analysis for document {document_id} deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to delete analysis: {str(e)}")


@router.get(
    "/analysis/stats",
    summary="Get analysis storage statistics",
    description="Get statistics about stored analysis results",
    responses={
        200: {"description": "Statistics retrieved successfully"}
    }
)
async def get_analysis_stats():
    """Get statistics about stored analysis results"""
    try:
        stats = analysis_storage_service.get_storage_stats()
        return stats
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get analysis statistics: {str(e)}")


@router.delete(
    "/analysis/all",
    summary="Clear all analysis results",
    description="Delete all stored analysis results",
    responses={
        200: {"description": "All analyses cleared successfully"},
        500: {"description": "Failed to clear analyses"}
    }
)
async def clear_all_analyses():
    """Clear all stored analysis results"""
    try:
        success = analysis_storage_service.clear_all_analyses()
        if not success:
            raise HTTPException(status_code=500, detail="Failed to clear all analyses")
        
        return {"message": "All analysis results cleared successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to clear analyses: {str(e)}")