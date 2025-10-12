#!/usr/bin/env python3
"""
Document Text Extractor - Service for extracting text from case documents

This service handles:
- Text extraction from various document formats (PDF, TXT, DOCX)
- Document retrieval from the file system
- Error handling for document processing failures
- Support for existing document storage structure
"""

import json
import os
from pathlib import Path
from typing import Dict, List, Any, Optional
import logging


logger = logging.getLogger(__name__)


class DocumentExtractionError(Exception):
    """Custom exception for document extraction errors."""
    pass


class DocumentExtractor:
    """Service for extracting text content from case documents."""
    
    def __init__(self):
        """Initialize the Document Extractor."""
        self.backend_dir = Path(__file__).parent.parent.parent
        self.documents_index_path = self.backend_dir / "data" / "cases" / "case_documents" / "case_documents_index.json"
        self.documents_base_path = self.backend_dir / "data" / "cases" / "case_documents"
    
    def extract_text(self, case_id: str, document_id: str) -> Optional[str]:
        """
        Extract text content from a specific document.
        
        Args:
            case_id: The ID of the case
            document_id: The ID of the document to extract
            
        Returns:
            Extracted text content or None if extraction fails
            
        Raises:
            DocumentExtractionError: If document cannot be processed
        """
        try:
            logger.info(f"Extracting text from document {document_id} for case {case_id}")
            
            # Find document metadata
            document_info = self._get_document_info(document_id)
            if not document_info:
                raise DocumentExtractionError(f"Document {document_id} not found in index")
            
            # Verify document belongs to the case
            if document_info.get('case_id') != case_id:
                raise DocumentExtractionError(f"Document {document_id} does not belong to case {case_id}")
            
            # Get document file path
            document_path = self._get_document_path(document_info)
            if not document_path or not document_path.exists():
                raise DocumentExtractionError(f"Document file not found: {document_path}")
            
            # Extract text based on file type
            text_content = self._extract_text_by_type(document_path, document_info.get('type', ''))
            
            if text_content:
                logger.info(f"Successfully extracted {len(text_content)} characters from document {document_id}")
                return text_content
            else:
                logger.warning(f"No text content extracted from document {document_id}")
                return None
                
        except DocumentExtractionError:
            raise
        except Exception as e:
            logger.error(f"Unexpected error extracting text from document {document_id}: {str(e)}")
            raise DocumentExtractionError(f"Unexpected error: {str(e)}")
    
    def extract_all_case_documents(self, case_id: str) -> List[Dict[str, str]]:
        """
        Extract text from all documents associated with a case.
        
        Args:
            case_id: The ID of the case
            
        Returns:
            List of dictionaries with document_id and content
        """
        try:
            logger.info(f"Extracting text from all documents for case {case_id}")
            
            # Get all documents for the case
            case_documents = self._get_case_documents(case_id)
            if not case_documents:
                logger.warning(f"No documents found for case {case_id}")
                return []
            
            extracted_documents = []
            
            for doc_info in case_documents:
                document_id = doc_info.get('id')
                try:
                    text_content = self.extract_text(case_id, document_id)
                    if text_content:
                        extracted_documents.append({
                            'document_id': document_id,
                            'document_name': doc_info.get('name', ''),
                            'document_type': doc_info.get('type', ''),
                            'content': text_content
                        })
                except DocumentExtractionError as e:
                    logger.warning(f"Failed to extract text from document {document_id}: {str(e)}")
                    continue
            
            logger.info(f"Successfully extracted text from {len(extracted_documents)} documents for case {case_id}")
            return extracted_documents
            
        except Exception as e:
            logger.error(f"Error extracting case documents for {case_id}: {str(e)}")
            return []
    
    def get_document_info(self, document_id: str) -> Optional[Dict[str, Any]]:
        """
        Get metadata information for a document.
        
        Args:
            document_id: The ID of the document
            
        Returns:
            Document metadata or None if not found
        """
        return self._get_document_info(document_id)
    
    def _get_document_info(self, document_id: str) -> Optional[Dict[str, Any]]:
        """Load document metadata from the index."""
        try:
            if not self.documents_index_path.exists():
                logger.error("Documents index file not found")
                return None
            
            with open(self.documents_index_path, 'r', encoding='utf-8') as f:
                index_data = json.load(f)
            
            documents = index_data.get('case_documents', [])
            return next((doc for doc in documents if doc.get('id') == document_id), None)
            
        except Exception as e:
            logger.error(f"Error loading document info for {document_id}: {str(e)}")
            return None
    
    def _get_case_documents(self, case_id: str) -> List[Dict[str, Any]]:
        """Get all documents for a specific case."""
        try:
            if not self.documents_index_path.exists():
                logger.error("Documents index file not found")
                return []
            
            with open(self.documents_index_path, 'r', encoding='utf-8') as f:
                index_data = json.load(f)
            
            documents = index_data.get('case_documents', [])
            return [doc for doc in documents if doc.get('case_id') == case_id]
            
        except Exception as e:
            logger.error(f"Error loading case documents for {case_id}: {str(e)}")
            return []
    
    def _get_document_path(self, document_info: Dict[str, Any]) -> Optional[Path]:
        """Get the full file path for a document."""
        try:
            # Check if full_content_path is provided in the document info
            if 'full_content_path' in document_info:
                # Path is relative to backend directory
                relative_path = document_info['full_content_path']
                
                # The path in the index is already relative to backend dir
                # e.g., "data/case_documents/case-001/doc-001_employment_contract_sarah_chen.txt"
                full_path = self.backend_dir / relative_path
                return full_path
            
            # Fallback: construct path from case_id and document_id
            case_id = document_info.get('case_id')
            document_id = document_info.get('id')
            document_name = document_info.get('name', '').lower().replace(' ', '_').replace('-', '_')
            
            # Try common file extensions
            for ext in ['.txt', '.pdf', '.docx']:
                filename = f"{document_id}_{document_name}{ext}"
                full_path = self.documents_base_path / case_id / filename
                if full_path.exists():
                    return full_path
            
            return None
            
        except Exception as e:
            logger.error(f"Error constructing document path: {str(e)}")
            return None
    
    def _extract_text_by_type(self, document_path: Path, document_type: str) -> Optional[str]:
        """
        Extract text content based on file type.
        
        Args:
            document_path: Path to the document file
            document_type: Type of document (for context)
            
        Returns:
            Extracted text content
        """
        try:
            file_extension = document_path.suffix.lower()
            
            if file_extension == '.txt':
                return self._extract_text_from_txt(document_path)
            elif file_extension == '.pdf':
                return self._extract_text_from_pdf(document_path)
            elif file_extension in ['.docx', '.doc']:
                return self._extract_text_from_docx(document_path)
            else:
                # Try to read as text file as fallback
                logger.warning(f"Unknown file type {file_extension}, attempting to read as text")
                return self._extract_text_from_txt(document_path)
                
        except Exception as e:
            logger.error(f"Error extracting text from {document_path}: {str(e)}")
            raise DocumentExtractionError(f"Failed to extract text: {str(e)}")
    
    def _extract_text_from_txt(self, document_path: Path) -> str:
        """Extract text from a TXT file."""
        try:
            with open(document_path, 'r', encoding='utf-8') as f:
                content = f.read()
            return content.strip()
        except UnicodeDecodeError:
            # Try with different encoding
            try:
                with open(document_path, 'r', encoding='latin-1') as f:
                    content = f.read()
                return content.strip()
            except Exception as e:
                raise DocumentExtractionError(f"Failed to read text file with multiple encodings: {str(e)}")
        except Exception as e:
            raise DocumentExtractionError(f"Failed to read text file: {str(e)}")
    
    def _extract_text_from_pdf(self, document_path: Path) -> str:
        """
        Extract text from a PDF file.
        
        Note: This is a placeholder implementation. In a production environment,
        you would use a library like PyPDF2, pdfplumber, or pymupdf.
        """
        try:
            # For now, we'll try to read it as text (in case it's actually a text file with .pdf extension)
            # In production, implement proper PDF text extraction
            logger.warning(f"PDF extraction not fully implemented for {document_path}")
            
            # Try reading as text first (some files might be misnamed)
            try:
                return self._extract_text_from_txt(document_path)
            except:
                pass
            
            # TODO: Implement proper PDF text extraction using PyPDF2 or similar
            # For now, return a placeholder message
            return f"[PDF content extraction not implemented - file: {document_path.name}]"
            
        except Exception as e:
            raise DocumentExtractionError(f"Failed to extract PDF text: {str(e)}")
    
    def _extract_text_from_docx(self, document_path: Path) -> str:
        """
        Extract text from a DOCX file.
        
        Note: This is a placeholder implementation. In a production environment,
        you would use a library like python-docx.
        """
        try:
            # For now, we'll try to read it as text (in case it's actually a text file with .docx extension)
            # In production, implement proper DOCX text extraction
            logger.warning(f"DOCX extraction not fully implemented for {document_path}")
            
            # Try reading as text first (some files might be misnamed)
            try:
                return self._extract_text_from_txt(document_path)
            except:
                pass
            
            # TODO: Implement proper DOCX text extraction using python-docx
            # For now, return a placeholder message
            return f"[DOCX content extraction not implemented - file: {document_path.name}]"
            
        except Exception as e:
            raise DocumentExtractionError(f"Failed to extract DOCX text: {str(e)}")
    
    def get_supported_formats(self) -> List[str]:
        """
        Get list of supported document formats.
        
        Returns:
            List of supported file extensions
        """
        return ['.txt', '.pdf', '.docx', '.doc']
    
    def validate_document_access(self, case_id: str, document_id: str) -> bool:
        """
        Validate that a document can be accessed for the given case.
        
        Args:
            case_id: The ID of the case
            document_id: The ID of the document
            
        Returns:
            True if document can be accessed, False otherwise
        """
        try:
            document_info = self._get_document_info(document_id)
            if not document_info:
                return False
            
            # Check if document belongs to the case
            if document_info.get('case_id') != case_id:
                return False
            
            # Check if file exists
            document_path = self._get_document_path(document_info)
            return document_path is not None and document_path.exists()
            
        except Exception as e:
            logger.error(f"Error validating document access: {str(e)}")
            return False