#!/usr/bin/env python3
"""
Unit tests for DocumentExtractor
"""

import pytest
import json
from unittest.mock import patch, mock_open, MagicMock
from pathlib import Path

from app.services.document_extractor import DocumentExtractor, DocumentExtractionError


class TestDocumentExtractor:
    """Test cases for DocumentExtractor"""

    @pytest.fixture
    def extractor(self):
        """Create DocumentExtractor instance for testing"""
        return DocumentExtractor()

    @pytest.fixture
    def mock_document_index(self):
        """Mock document index data"""
        return {
            "case_documents": [
                {
                    "id": "doc-001",
                    "case_id": "case-001",
                    "name": "Test Document",
                    "type": "Contract",
                    "full_content_path": "data/case_documents/case-001/doc-001_test.txt"
                },
                {
                    "id": "doc-002",
                    "case_id": "case-001",
                    "name": "Another Document",
                    "type": "Evidence",
                    "full_content_path": "data/case_documents/case-001/doc-002_another.pdf"
                },
                {
                    "id": "doc-003",
                    "case_id": "case-002",
                    "name": "Different Case Doc",
                    "type": "Email",
                    "full_content_path": "data/case_documents/case-002/doc-003_different.txt"
                }
            ]
        }

    def test_init(self, extractor):
        """Test DocumentExtractor initialization"""
        assert extractor.backend_dir is not None
        assert extractor.documents_index_path is not None
        assert extractor.documents_base_path is not None

    def test_extract_text_success(self, extractor, mock_document_index):
        """Test successful text extraction"""
        with patch("builtins.open", mock_open(read_data=json.dumps(mock_document_index))):
            with patch("pathlib.Path.exists", return_value=True):
                with patch.object(extractor, '_extract_text_by_type', return_value="Test document content"):
                    result = extractor.extract_text("case-001", "doc-001")
        
        assert result == "Test document content"

    @patch("builtins.open", new_callable=mock_open)
    @patch("pathlib.Path.exists", return_value=True)
    def test_extract_text_document_not_found(self, mock_exists, mock_file, extractor, mock_document_index):
        """Test text extraction when document is not found in index"""
        with patch("builtins.open", mock_open(read_data=json.dumps(mock_document_index))):
            with pytest.raises(DocumentExtractionError, match="Document nonexistent not found in index"):
                extractor.extract_text("case-001", "nonexistent")

    @patch("builtins.open", new_callable=mock_open)
    @patch("pathlib.Path.exists", return_value=True)
    def test_extract_text_wrong_case(self, mock_exists, mock_file, extractor, mock_document_index):
        """Test text extraction when document belongs to different case"""
        with patch("builtins.open", mock_open(read_data=json.dumps(mock_document_index))):
            with pytest.raises(DocumentExtractionError, match="Document doc-003 does not belong to case case-001"):
                extractor.extract_text("case-001", "doc-003")

    def test_extract_text_file_not_found(self, extractor, mock_document_index):
        """Test text extraction when document file doesn't exist"""
        with patch("builtins.open", mock_open(read_data=json.dumps(mock_document_index))):
            with patch("pathlib.Path.exists", return_value=True):  # Index exists
                with patch.object(extractor, '_get_document_path', return_value=None):
                    with pytest.raises(DocumentExtractionError, match="Document file not found"):
                        extractor.extract_text("case-001", "doc-001")

    def test_extract_all_case_documents_success(self, extractor, mock_document_index):
        """Test extracting all documents for a case"""
        with patch("builtins.open", mock_open(read_data=json.dumps(mock_document_index))):
            with patch.object(extractor, 'extract_text') as mock_extract:
                mock_extract.side_effect = ["Content 1", "Content 2"]
                
                result = extractor.extract_all_case_documents("case-001")
        
        assert len(result) == 2
        assert result[0]["document_id"] == "doc-001"
        assert result[0]["content"] == "Content 1"
        assert result[1]["document_id"] == "doc-002"
        assert result[1]["content"] == "Content 2"

    def test_extract_all_case_documents_no_documents(self, extractor):
        """Test extracting documents when case has no documents"""
        empty_index = {"case_documents": []}
        
        with patch("builtins.open", mock_open(read_data=json.dumps(empty_index))):
            result = extractor.extract_all_case_documents("case-001")
        
        assert result == []

    def test_extract_all_case_documents_with_failures(self, extractor, mock_document_index):
        """Test extracting documents when some extractions fail"""
        with patch("builtins.open", mock_open(read_data=json.dumps(mock_document_index))):
            with patch.object(extractor, 'extract_text') as mock_extract:
                # First extraction succeeds, second fails
                mock_extract.side_effect = ["Content 1", DocumentExtractionError("Failed")]
                
                result = extractor.extract_all_case_documents("case-001")
        
        assert len(result) == 1
        assert result[0]["document_id"] == "doc-001"
        assert result[0]["content"] == "Content 1"

    def test_get_document_info_success(self, extractor, mock_document_index):
        """Test getting document info successfully"""
        with patch("builtins.open", mock_open(read_data=json.dumps(mock_document_index))):
            with patch("pathlib.Path.exists", return_value=True):
                result = extractor.get_document_info("doc-001")
        
        assert result is not None
        assert result["id"] == "doc-001"
        assert result["case_id"] == "case-001"
        assert result["name"] == "Test Document"

    def test_get_document_info_not_found(self, extractor, mock_document_index):
        """Test getting document info when document not found"""
        with patch("builtins.open", mock_open(read_data=json.dumps(mock_document_index))):
            with patch("pathlib.Path.exists", return_value=True):
                result = extractor.get_document_info("nonexistent")
        
        assert result is None

    @patch("pathlib.Path.exists", return_value=False)
    def test_get_document_info_index_not_found(self, mock_exists, extractor):
        """Test getting document info when index file doesn't exist"""
        result = extractor.get_document_info("doc-001")
        
        assert result is None

    def test_get_case_documents_success(self, extractor, mock_document_index):
        """Test getting all documents for a case"""
        with patch("builtins.open", mock_open(read_data=json.dumps(mock_document_index))):
            with patch("pathlib.Path.exists", return_value=True):
                result = extractor._get_case_documents("case-001")
        
        assert len(result) == 2
        assert result[0]["id"] == "doc-001"
        assert result[1]["id"] == "doc-002"

    def test_get_case_documents_no_documents(self, extractor, mock_document_index):
        """Test getting documents for case with no documents"""
        with patch("builtins.open", mock_open(read_data=json.dumps(mock_document_index))):
            with patch("pathlib.Path.exists", return_value=True):
                result = extractor._get_case_documents("nonexistent-case")
        
        assert result == []

    def test_get_document_path_with_full_path(self, extractor):
        """Test getting document path when full_content_path is provided"""
        document_info = {
            "full_content_path": "data/case_documents/case-001/doc-001_test.txt"
        }
        
        result = extractor._get_document_path(document_info)
        
        assert result is not None
        assert "doc-001_test.txt" in str(result)

    def test_get_document_path_fallback(self, extractor):
        """Test getting document path using fallback method"""
        document_info = {
            "case_id": "case-001",
            "id": "doc-001",
            "name": "Test Document"
        }
        
        with patch("pathlib.Path.exists", return_value=True):
            result = extractor._get_document_path(document_info)
        
        assert result is not None

    def test_extract_text_from_txt_success(self, extractor):
        """Test extracting text from TXT file"""
        test_content = "This is test content"
        
        with patch("builtins.open", mock_open(read_data=test_content)):
            result = extractor._extract_text_from_txt(Path("test.txt"))
        
        assert result == test_content

    def test_extract_text_from_txt_encoding_error(self, extractor):
        """Test extracting text from TXT file with encoding issues"""
        with patch("builtins.open") as mock_file:
            # First call raises UnicodeDecodeError, second succeeds
            mock_file.side_effect = [
                UnicodeDecodeError('utf-8', b'', 0, 1, 'invalid start byte'),
                mock_open(read_data="Content with latin-1").return_value
            ]
            
            result = extractor._extract_text_from_txt(Path("test.txt"))
            
            assert result == "Content with latin-1"

    def test_extract_text_from_pdf_placeholder(self, extractor):
        """Test PDF extraction placeholder implementation"""
        with patch.object(extractor, '_extract_text_from_txt', return_value="PDF as text"):
            result = extractor._extract_text_from_pdf(Path("test.pdf"))
            
            assert result == "PDF as text"

    def test_extract_text_from_docx_placeholder(self, extractor):
        """Test DOCX extraction placeholder implementation"""
        with patch.object(extractor, '_extract_text_from_txt', return_value="DOCX as text"):
            result = extractor._extract_text_from_docx(Path("test.docx"))
            
            assert result == "DOCX as text"

    def test_get_supported_formats(self, extractor):
        """Test getting supported file formats"""
        formats = extractor.get_supported_formats()
        
        assert '.txt' in formats
        assert '.pdf' in formats
        assert '.docx' in formats
        assert '.doc' in formats

    def test_validate_document_access_success(self, extractor, mock_document_index):
        """Test successful document access validation"""
        with patch("builtins.open", mock_open(read_data=json.dumps(mock_document_index))):
            with patch("pathlib.Path.exists", return_value=True):
                result = extractor.validate_document_access("case-001", "doc-001")
        
        assert result is True

    def test_validate_document_access_wrong_case(self, extractor, mock_document_index):
        """Test document access validation for wrong case"""
        with patch("builtins.open", mock_open(read_data=json.dumps(mock_document_index))):
            result = extractor.validate_document_access("case-001", "doc-003")
        
        assert result is False

    def test_validate_document_access_file_not_exists(self, extractor, mock_document_index):
        """Test document access validation when file doesn't exist"""
        with patch("builtins.open", mock_open(read_data=json.dumps(mock_document_index))):
            with patch("pathlib.Path.exists", return_value=False):
                result = extractor.validate_document_access("case-001", "doc-001")
        
        assert result is False

    def test_validate_document_access_document_not_found(self, extractor, mock_document_index):
        """Test document access validation when document not in index"""
        with patch("builtins.open", mock_open(read_data=json.dumps(mock_document_index))):
            result = extractor.validate_document_access("case-001", "nonexistent")
        
        assert result is False

    def test_extract_text_unexpected_error(self, extractor, mock_document_index):
        """Test text extraction with unexpected error"""
        with patch("builtins.open", mock_open(read_data=json.dumps(mock_document_index))):
            with patch("pathlib.Path.exists", return_value=True):
                with patch.object(extractor, '_extract_text_by_type', side_effect=Exception("Unexpected error")):
                    with pytest.raises(DocumentExtractionError, match="Unexpected error"):
                        extractor.extract_text("case-001", "doc-001")

    def test_extract_all_case_documents_index_error(self, extractor):
        """Test extracting all documents when index loading fails"""
        with patch.object(extractor, '_get_case_documents', side_effect=Exception("Index error")):
            result = extractor.extract_all_case_documents("case-001")
            
            assert result == []

    def test_get_document_info_json_decode_error(self, extractor):
        """Test getting document info with invalid JSON in index"""
        with patch("builtins.open", mock_open(read_data="invalid json")):
            with patch("pathlib.Path.exists", return_value=True):
                result = extractor.get_document_info("doc-001")
        
        assert result is None

    def test_get_case_documents_json_decode_error(self, extractor):
        """Test getting case documents with invalid JSON in index"""
        with patch("builtins.open", mock_open(read_data="invalid json")):
            with patch("pathlib.Path.exists", return_value=True):
                result = extractor._get_case_documents("case-001")
        
        assert result == []

    def test_get_document_path_exception(self, extractor):
        """Test getting document path with exception"""
        document_info = {"invalid": "data"}  # Missing required fields
        
        result = extractor._get_document_path(document_info)
        
        assert result is None

    def test_extract_text_by_type_unknown_extension(self, extractor):
        """Test extracting text from unknown file type"""
        document_path = Path("test.xyz")  # Unknown extension
        
        with patch.object(extractor, '_extract_text_from_txt', return_value="fallback content"):
            result = extractor._extract_text_by_type(document_path, "Unknown")
            
            assert result == "fallback content"

    def test_extract_text_by_type_extraction_failure(self, extractor):
        """Test text extraction when underlying extraction fails"""
        document_path = Path("test.txt")
        
        with patch.object(extractor, '_extract_text_from_txt', side_effect=Exception("Extraction failed")):
            with pytest.raises(DocumentExtractionError, match="Failed to extract text"):
                extractor._extract_text_by_type(document_path, "Text")

    def test_extract_text_from_txt_file_not_found(self, extractor):
        """Test extracting text from non-existent TXT file"""
        with patch("builtins.open", side_effect=FileNotFoundError("File not found")):
            with pytest.raises(DocumentExtractionError, match="Failed to read text file"):
                extractor._extract_text_from_txt(Path("nonexistent.txt"))

    def test_extract_text_from_txt_permission_error(self, extractor):
        """Test extracting text from TXT file with permission error"""
        with patch("builtins.open", side_effect=PermissionError("Permission denied")):
            with pytest.raises(DocumentExtractionError, match="Failed to read text file"):
                extractor._extract_text_from_txt(Path("restricted.txt"))

    def test_extract_text_from_txt_multiple_encoding_failures(self, extractor):
        """Test extracting text when both UTF-8 and Latin-1 fail"""
        with patch("builtins.open") as mock_file:
            # Both encodings fail
            mock_file.side_effect = [
                UnicodeDecodeError('utf-8', b'', 0, 1, 'invalid start byte'),
                UnicodeDecodeError('latin-1', b'', 0, 1, 'invalid start byte')
            ]
            
            with pytest.raises(DocumentExtractionError, match="Failed to read text file with multiple encodings"):
                extractor._extract_text_from_txt(Path("problematic.txt"))

    def test_extract_text_from_pdf_fallback_failure(self, extractor):
        """Test PDF extraction when text fallback also fails"""
        with patch.object(extractor, '_extract_text_from_txt', side_effect=Exception("Text extraction failed")):
            result = extractor._extract_text_from_pdf(Path("test.pdf"))
            
            # Should return placeholder message when fallback fails
            assert "[PDF content extraction not implemented" in result

    def test_extract_text_from_docx_fallback_failure(self, extractor):
        """Test DOCX extraction when text fallback also fails"""
        with patch.object(extractor, '_extract_text_from_txt', side_effect=Exception("Text extraction failed")):
            result = extractor._extract_text_from_docx(Path("test.docx"))
            
            # Should return placeholder message when fallback fails
            assert "[DOCX content extraction not implemented" in result

    def test_validate_document_access_exception(self, extractor):
        """Test document access validation with exception"""
        with patch.object(extractor, '_get_document_info', side_effect=Exception("Validation error")):
            result = extractor.validate_document_access("case-001", "doc-001")
            
            assert result is False

    def test_extract_all_case_documents_mixed_success_failure(self, extractor, mock_document_index):
        """Test extracting documents with mixed success and failure scenarios"""
        with patch("builtins.open", mock_open(read_data=json.dumps(mock_document_index))):
            with patch.object(extractor, 'extract_text') as mock_extract:
                # First succeeds, second fails with DocumentExtractionError
                # Only case-001 has 2 documents (doc-001 and doc-002)
                mock_extract.side_effect = [
                    "Content 1",
                    DocumentExtractionError("Extraction failed")
                ]
                
                result = extractor.extract_all_case_documents("case-001")
                
                # Should return only successful extractions (1 out of 2)
                assert len(result) == 1
                assert result[0]["content"] == "Content 1"

    def test_get_document_path_fallback_no_files_found(self, extractor):
        """Test document path fallback when no files are found"""
        document_info = {
            "case_id": "case-001",
            "id": "doc-001",
            "name": "Test Document"
        }
        
        with patch("pathlib.Path.exists", return_value=False):  # No files exist
            result = extractor._get_document_path(document_info)
            
            assert result is None

    def test_extract_text_empty_content(self, extractor, mock_document_index):
        """Test text extraction returning empty content"""
        with patch("builtins.open", mock_open(read_data=json.dumps(mock_document_index))):
            with patch("pathlib.Path.exists", return_value=True):
                with patch.object(extractor, '_extract_text_by_type', return_value=""):
                    result = extractor.extract_text("case-001", "doc-001")
                    
                    assert result is None  # Empty content should return None

    def test_extract_text_whitespace_only_content(self, extractor, mock_document_index):
        """Test text extraction with whitespace-only content"""
        with patch("builtins.open", mock_open(read_data=json.dumps(mock_document_index))):
            with patch("pathlib.Path.exists", return_value=True):
                with patch.object(extractor, '_extract_text_by_type', return_value="   \n\t  "):
                    result = extractor.extract_text("case-001", "doc-001")
                    
                    # The service returns the content as-is, it doesn't strip whitespace
                    assert result == "   \n\t  "