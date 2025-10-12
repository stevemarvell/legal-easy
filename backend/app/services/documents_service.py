#!/usr/bin/env python3
"""
DocumentsService - Document management service for the Legal AI System

This service handles document-related operations including:
- Loading case documents from JSON files
- Document content retrieval
- Document search and filtering
"""

import json
from pathlib import Path
from typing import Dict, List, Any, Optional


class DocumentsService:
    """Service for document management operations."""
    
    @staticmethod
    def load_case_documents(case_id: str) -> List[Dict[str, Any]]:
        """Load all documents for a specific case."""
        try:
            backend_dir = Path(__file__).parent.parent.parent
            case_docs_path = backend_dir / "data" / "cases" / "case_documents" / "case_documents_index.json"
            
            if not case_docs_path.exists():
                return []
            
            with open(case_docs_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                
                # Handle both flat array and nested structure
                if isinstance(data, dict) and 'case_documents' in data:
                    all_docs = data['case_documents']
                else:
                    all_docs = data
                
                # Filter documents for the specific case
                case_docs = [doc for doc in all_docs if doc.get('case_id') == case_id]
                return case_docs
        except Exception as e:
            print(f"Error loading case documents: {e}")
            return []
    
    @staticmethod
    def load_document_content(document_id: str) -> Optional[str]:
        """Load the full text content of a document."""
        try:
            backend_dir = Path(__file__).parent.parent.parent
            
            # First, find the document in the index to get its path
            case_docs_path = backend_dir / "data" / "cases" / "case_documents" / "case_documents_index.json"
            
            if not case_docs_path.exists():
                return None
            
            with open(case_docs_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Handle both flat array and nested structure
            if isinstance(data, dict) and 'case_documents' in data:
                all_docs = data['case_documents']
            else:
                all_docs = data
            
            # Find the document
            document = next((doc for doc in all_docs if doc.get('id') == document_id), None)
            if not document:
                return None
            
            # Load content from the document's file path
            if 'full_content_path' in document:
                content_path = backend_dir / "data" / document['full_content_path']
                if content_path.exists():
                    with open(content_path, 'r', encoding='utf-8') as f:
                        return f.read()
            
            # Fallback to content preview if full content not available
            return document.get('content_preview', '')
            
        except Exception as e:
            print(f"Error loading document content: {e}")
            return None
    
    @staticmethod
    def find_document_by_id(document_id: str) -> Optional[Dict[str, Any]]:
        """Find a document by ID across all cases."""
        try:
            backend_dir = Path(__file__).parent.parent.parent
            case_docs_path = backend_dir / "data" / "cases" / "case_documents" / "case_documents_index.json"
            
            if not case_docs_path.exists():
                return None
            
            with open(case_docs_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Handle both flat array and nested structure
            if isinstance(data, dict) and 'case_documents' in data:
                all_docs = data['case_documents']
            else:
                all_docs = data
            
            # Find the document
            document = next((doc for doc in all_docs if doc.get('id') == document_id), None)
            return document
            
        except Exception as e:
            print(f"Error finding document: {e}")
            return None
# 
Export the service class
__all__ = ['DocumentsService']