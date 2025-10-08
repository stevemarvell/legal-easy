from fastapi import APIRouter
from typing import List
from app.models.document import Document, DocumentAnalysis
from app.services.document_service import DocumentService

router = APIRouter(prefix="/documents", tags=["documents"])
document_service = DocumentService()


@router.get("/cases/{case_id}/documents", response_model=List[Document])
async def get_case_documents(case_id: str):
    """Get all documents for a case"""
    # Implementation will be added in later tasks
    pass


@router.get("/{document_id}", response_model=Document)
async def get_document(document_id: str):
    """Get a specific document"""
    # Implementation will be added in later tasks
    pass


@router.get("/{document_id}/analysis", response_model=DocumentAnalysis)
async def get_document_analysis(document_id: str):
    """Get AI analysis for a document"""
    # Implementation will be added in later tasks
    pass