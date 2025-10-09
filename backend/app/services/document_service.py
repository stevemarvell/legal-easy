import json
import os
from typing import List, Optional
from app.models.document import Document, DocumentAnalysis


class DocumentService:
    """Service for managing legal documents"""
    
    def __init__(self):
        self._documents_cache = None
        self._analyses_cache = None
        self._documents_file = os.path.join(os.path.dirname(__file__), "..", "data", "demo_documents.json")
        self._analyses_file = os.path.join(os.path.dirname(__file__), "..", "data", "demo_document_analysis.json")
    
    def _load_documents(self) -> List[Document]:
        """Load documents from JSON file with caching"""
        if self._documents_cache is None:
            try:
                with open(self._documents_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self._documents_cache = [Document(**doc_data) for doc_data in data["documents"]]
            except FileNotFoundError:
                raise FileNotFoundError(f"Demo documents file not found: {self._documents_file}")
            except json.JSONDecodeError as e:
                raise ValueError(f"Invalid JSON in demo documents file: {e}")
        return self._documents_cache
    
    def _load_analyses(self) -> List[DocumentAnalysis]:
        """Load document analyses from JSON file with caching"""
        if self._analyses_cache is None:
            try:
                with open(self._analyses_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self._analyses_cache = [DocumentAnalysis(**analysis_data) for analysis_data in data["document_analyses"]]
            except FileNotFoundError:
                # Demo analysis file deleted - return empty list
                self._analyses_cache = []
            except json.JSONDecodeError as e:
                raise ValueError(f"Invalid JSON in demo document analyses file: {e}")
        return self._analyses_cache
    
    def get_case_documents(self, case_id: str) -> List[Document]:
        """Get all documents for a specific case"""
        documents = self._load_documents()
        return [doc for doc in documents if doc.case_id == case_id]
    
    def get_document_by_id(self, doc_id: str) -> Optional[Document]:
        """Get a specific document by ID"""
        documents = self._load_documents()
        for doc in documents:
            if doc.id == doc_id:
                return doc
        return None
    
    def get_document_analysis(self, doc_id: str) -> Optional[DocumentAnalysis]:
        """Get AI analysis results for a document"""
        analyses = self._load_analyses()
        for analysis in analyses:
            if analysis.document_id == doc_id:
                return analysis
        return None