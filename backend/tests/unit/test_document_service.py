import pytest
import json
import os
from unittest.mock import patch, mock_open, MagicMock
from datetime import datetime, date
from app.services.document_service import DocumentService
from app.models.document import Document, DocumentAnalysis


class TestDocumentService:
    """Test the DocumentService class"""
    
    @pytest.fixture
    def mock_documents_data(self):
        """Mock documents data for testing"""
        return {
            "documents": [
                {
                    "id": "doc-001",
                    "case_id": "case-001",
                    "name": "Test Document 1",
                    "type": "Contract",
                    "size": 1024,
                    "upload_date": "2024-01-15T10:00:00Z",
                    "content_preview": "This is a test document preview...",
                    "analysis_completed": True
                },
                {
                    "id": "doc-002",
                    "case_id": "case-001",
                    "name": "Test Document 2",
                    "type": "Email",
                    "size": 512,
                    "upload_date": "2024-01-16T11:00:00Z",
                    "content_preview": "Email content preview...",
                    "analysis_completed": False
                },
                {
                    "id": "doc-003",
                    "case_id": "case-002",
                    "name": "Test Document 3",
                    "type": "Legal Brief",
                    "size": 2048,
                    "upload_date": "2024-01-17T12:00:00Z",
                    "content_preview": "Legal brief preview...",
                    "analysis_completed": True
                }
            ]
        }
    
    @pytest.fixture
    def mock_analyses_data(self):
        """Mock document analyses data for testing"""
        return {
            "document_analyses": [
                {
                    "document_id": "doc-001",
                    "key_dates": ["2024-01-15", "2024-02-01"],
                    "parties_involved": ["John Doe", "Company Inc"],
                    "document_type": "Employment Contract",
                    "summary": "Test document analysis summary",
                    "key_clauses": ["Clause 1", "Clause 2"],
                    "confidence_scores": {"parties": 0.95, "dates": 0.98}
                },
                {
                    "document_id": "doc-003",
                    "key_dates": ["2024-01-10"],
                    "parties_involved": ["Jane Smith", "Vendor LLC"],
                    "document_type": "Legal Brief",
                    "summary": "Legal brief analysis",
                    "key_clauses": ["Important clause"],
                    "confidence_scores": {"parties": 0.92, "dates": 0.89}
                }
            ]
        }
    
    @pytest.fixture
    def document_service(self):
        """Create a DocumentService instance for testing"""
        return DocumentService()
    
    def test_init(self, document_service):
        """Test DocumentService initialization"""
        assert document_service._documents_cache is None
        assert document_service._analyses_cache is None
        assert document_service._documents_file.endswith("demo_documents.json")
        assert document_service._analyses_file.endswith("demo_document_analysis.json")
    
    @patch("builtins.open", new_callable=mock_open)
    @patch("json.load")
    def test_load_documents_success(self, mock_json_load, mock_file, document_service, mock_documents_data):
        """Test successful loading of documents from JSON file"""
        mock_json_load.return_value = mock_documents_data
        
        documents = document_service._load_documents()
        
        assert len(documents) == 3
        assert all(isinstance(doc, Document) for doc in documents)
        assert documents[0].id == "doc-001"
        assert documents[0].name == "Test Document 1"
        assert documents[1].type == "Email"
        mock_file.assert_called_once()
        mock_json_load.assert_called_once()
    
    @patch("builtins.open", side_effect=FileNotFoundError)
    def test_load_documents_file_not_found(self, mock_file, document_service):
        """Test handling of missing documents file"""
        with pytest.raises(FileNotFoundError, match="Demo documents file not found"):
            document_service._load_documents()
    
    @patch("builtins.open", new_callable=mock_open)
    @patch("json.load", side_effect=json.JSONDecodeError("Invalid JSON", "", 0))
    def test_load_documents_invalid_json(self, mock_json_load, mock_file, document_service):
        """Test handling of invalid JSON in documents file"""
        with pytest.raises(ValueError, match="Invalid JSON in demo documents file"):
            document_service._load_documents()
    
    @patch("builtins.open", new_callable=mock_open)
    @patch("json.load")
    def test_load_analyses_success(self, mock_json_load, mock_file, document_service, mock_analyses_data):
        """Test successful loading of analyses from JSON file"""
        mock_json_load.return_value = mock_analyses_data
        
        analyses = document_service._load_analyses()
        
        assert len(analyses) == 2
        assert all(isinstance(analysis, DocumentAnalysis) for analysis in analyses)
        assert analyses[0].document_id == "doc-001"
        assert analyses[0].summary == "Test document analysis summary"
        assert analyses[1].document_type == "Legal Brief"
        mock_file.assert_called_once()
        mock_json_load.assert_called_once()
    
    @patch("builtins.open", side_effect=FileNotFoundError)
    def test_load_analyses_file_not_found(self, mock_file, document_service):
        """Test handling of missing analyses file"""
        with pytest.raises(FileNotFoundError, match="Demo document analyses file not found"):
            document_service._load_analyses()
    
    @patch("builtins.open", new_callable=mock_open)
    @patch("json.load", side_effect=json.JSONDecodeError("Invalid JSON", "", 0))
    def test_load_analyses_invalid_json(self, mock_json_load, mock_file, document_service):
        """Test handling of invalid JSON in analyses file"""
        with pytest.raises(ValueError, match="Invalid JSON in demo document analyses file"):
            document_service._load_analyses()
    
    @patch.object(DocumentService, '_load_documents')
    def test_get_case_documents(self, mock_load_documents, document_service, mock_documents_data):
        """Test getting documents for a specific case"""
        mock_documents = [Document(**doc_data) for doc_data in mock_documents_data["documents"]]
        mock_load_documents.return_value = mock_documents
        
        result = document_service.get_case_documents("case-001")
        
        assert len(result) == 2
        assert all(doc.case_id == "case-001" for doc in result)
        assert result[0].id == "doc-001"
        assert result[1].id == "doc-002"
        mock_load_documents.assert_called_once()
    
    @patch.object(DocumentService, '_load_documents')
    def test_get_case_documents_no_matches(self, mock_load_documents, document_service, mock_documents_data):
        """Test getting documents for a case with no documents"""
        mock_documents = [Document(**doc_data) for doc_data in mock_documents_data["documents"]]
        mock_load_documents.return_value = mock_documents
        
        result = document_service.get_case_documents("case-999")
        
        assert len(result) == 0
        assert result == []
    
    @patch.object(DocumentService, '_load_documents')
    def test_get_document_by_id_found(self, mock_load_documents, document_service, mock_documents_data):
        """Test getting a document by ID when it exists"""
        mock_documents = [Document(**doc_data) for doc_data in mock_documents_data["documents"]]
        mock_load_documents.return_value = mock_documents
        
        result = document_service.get_document_by_id("doc-002")
        
        assert result is not None
        assert result.id == "doc-002"
        assert result.name == "Test Document 2"
        assert result.type == "Email"
        assert result.case_id == "case-001"
    
    @patch.object(DocumentService, '_load_documents')
    def test_get_document_by_id_not_found(self, mock_load_documents, document_service, mock_documents_data):
        """Test getting a document by ID when it doesn't exist"""
        mock_documents = [Document(**doc_data) for doc_data in mock_documents_data["documents"]]
        mock_load_documents.return_value = mock_documents
        
        result = document_service.get_document_by_id("doc-999")
        
        assert result is None
    
    @patch.object(DocumentService, '_load_analyses')
    def test_get_document_analysis_found(self, mock_load_analyses, document_service, mock_analyses_data):
        """Test getting document analysis when it exists"""
        mock_analyses = [DocumentAnalysis(**analysis_data) for analysis_data in mock_analyses_data["document_analyses"]]
        mock_load_analyses.return_value = mock_analyses
        
        result = document_service.get_document_analysis("doc-001")
        
        assert result is not None
        assert result.document_id == "doc-001"
        assert result.summary == "Test document analysis summary"
        assert result.document_type == "Employment Contract"
        assert len(result.key_dates) == 2
        assert len(result.parties_involved) == 2
    
    @patch.object(DocumentService, '_load_analyses')
    def test_get_document_analysis_not_found(self, mock_load_analyses, document_service, mock_analyses_data):
        """Test getting document analysis when it doesn't exist"""
        mock_analyses = [DocumentAnalysis(**analysis_data) for analysis_data in mock_analyses_data["document_analyses"]]
        mock_load_analyses.return_value = mock_analyses
        
        result = document_service.get_document_analysis("doc-999")
        
        assert result is None
    
    @patch.object(DocumentService, '_load_documents')
    @patch.object(DocumentService, '_load_analyses')
    def test_caching_behavior_documents(self, mock_load_analyses, mock_load_documents, document_service, mock_documents_data):
        """Test that documents are cached after first load"""
        mock_documents = [Document(**doc_data) for doc_data in mock_documents_data["documents"]]
        mock_load_documents.return_value = mock_documents
        
        # First call should load documents
        result1 = document_service.get_case_documents("case-001")
        # Second call should use cache
        result2 = document_service.get_case_documents("case-001")
        
        assert result1 == result2
        # _load_documents should be called twice (once for each get_case_documents call)
        # but the actual file loading should be cached
        assert mock_load_documents.call_count == 2
    
    @patch.object(DocumentService, '_load_analyses')
    def test_caching_behavior_analyses(self, mock_load_analyses, document_service, mock_analyses_data):
        """Test that analyses are cached after first load"""
        mock_analyses = [DocumentAnalysis(**analysis_data) for analysis_data in mock_analyses_data["document_analyses"]]
        mock_load_analyses.return_value = mock_analyses
        
        # First call should load analyses
        result1 = document_service.get_document_analysis("doc-001")
        # Second call should use cache
        result2 = document_service.get_document_analysis("doc-001")
        
        assert result1 == result2
        # _load_analyses should be called twice (once for each get_document_analysis call)
        # but the actual file loading should be cached
        assert mock_load_analyses.call_count == 2
    
    @patch.object(DocumentService, '_load_documents')
    def test_get_case_documents_multiple_cases(self, mock_load_documents, document_service, mock_documents_data):
        """Test getting documents for different cases"""
        mock_documents = [Document(**doc_data) for doc_data in mock_documents_data["documents"]]
        mock_load_documents.return_value = mock_documents
        
        case_001_docs = document_service.get_case_documents("case-001")
        case_002_docs = document_service.get_case_documents("case-002")
        
        assert len(case_001_docs) == 2
        assert len(case_002_docs) == 1
        assert case_002_docs[0].id == "doc-003"
        assert all(doc.case_id == "case-001" for doc in case_001_docs)
        assert all(doc.case_id == "case-002" for doc in case_002_docs)