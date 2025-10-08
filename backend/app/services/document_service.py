from typing import List
from app.models.document import Document, DocumentAnalysis


class DocumentService:
    """Service for managing legal documents"""
    
    def get_case_documents(self, case_id: str) -> List[Document]:
        """Get all documents for a specific case"""
        # Implementation will be added in later tasks
        pass
    
    def get_document_by_id(self, doc_id: str) -> Document:
        """Get a specific document by ID"""
        # Implementation will be added in later tasks
        pass
    
    def get_document_analysis(self, doc_id: str) -> DocumentAnalysis:
        """Get AI analysis results for a document"""
        # Implementation will be added in later tasks
        pass