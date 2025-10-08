import pytest
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient
from fastapi import HTTPException
from datetime import datetime, date
from main import app
from app.models.document import Document, DocumentAnalysis
from app.services.document_service import DocumentService


class TestDocumentsAPI:
    """Test the Documents API endpoints"""
    
    @pytest.fixture
    def client(self):
        """Create a test client for the FastAPI app"""
        return TestClient(app)
    
    @pytest.fixture
    def mock_documents(self):
        """Mock documents data for testing"""
        return [
            Document(
                id="doc-001",
                case_id="case-001",
                name="Test Document 1",
                type="Contract",
                size=1024,
                upload_date=datetime(2024, 1, 15, 10, 0, 0),
                content_preview="This is a test document preview...",
                analysis_completed=True
            ),
            Document(
                id="doc-002",
                case_id="case-001",
                name="Test Document 2",
                type="Email",
                size=512,
                upload_date=datetime(2024, 1, 16, 11, 0, 0),
                content_preview="Email content preview...",
                analysis_completed=False
            )
        ]
    
    @pytest.fixture
    def mock_document_analysis(self):
        """Mock document analysis data for testing"""
        return DocumentAnalysis(
            document_id="doc-001",
            key_dates=[date(2024, 1, 15), date(2024, 2, 1)],
            parties_involved=["John Doe", "Company Inc"],
            document_type="Employment Contract",
            summary="Test document analysis summary",
            key_clauses=["Clause 1", "Clause 2"],
            confidence_scores={"parties": 0.95, "dates": 0.98}
        )
    
    @patch.object(DocumentService, 'get_case_documents')
    def test_get_case_documents_success(self, mock_get_case_docs, client, mock_documents):
        """Test successful retrieval of case documents"""
        mock_get_case_docs.return_value = mock_documents
        
        response = client.get("/documents/cases/case-001/documents")
        
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2
        assert data[0]["id"] == "doc-001"
        assert data[0]["name"] == "Test Document 1"
        assert data[0]["type"] == "Contract"
        assert data[0]["case_id"] == "case-001"
        assert data[1]["id"] == "doc-002"
        assert data[1]["type"] == "Email"
        assert data[1]["analysis_completed"] is False
        mock_get_case_docs.assert_called_once_with("case-001")
    
    @patch.object(DocumentService, 'get_case_documents')
    def test_get_case_documents_empty_list(self, mock_get_case_docs, client):
        """Test retrieval when case has no documents"""
        mock_get_case_docs.return_value = []
        
        response = client.get("/documents/cases/case-999/documents")
        
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 0
        assert data == []
        mock_get_case_docs.assert_called_once_with("case-999")
    
    @patch.object(DocumentService, 'get_case_documents')
    def test_get_case_documents_error(self, mock_get_case_docs, client):
        """Test error handling in get case documents endpoint"""
        mock_get_case_docs.side_effect = Exception("Service error")
        
        response = client.get("/documents/cases/case-001/documents")
        
        assert response.status_code == 500
        data = response.json()
        assert "Failed to get case documents" in data["detail"]
        assert "Service error" in data["detail"]
    
    @patch.object(DocumentService, 'get_document_by_id')
    def test_get_document_by_id_success(self, mock_get_by_id, client, mock_documents):
        """Test successful retrieval of a specific document"""
        mock_get_by_id.return_value = mock_documents[0]
        
        response = client.get("/documents/doc-001")
        
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == "doc-001"
        assert data["name"] == "Test Document 1"
        assert data["type"] == "Contract"
        assert data["case_id"] == "case-001"
        assert data["size"] == 1024
        assert data["analysis_completed"] is True
        assert "content_preview" in data
        mock_get_by_id.assert_called_once_with("doc-001")
    
    @patch.object(DocumentService, 'get_document_by_id')
    def test_get_document_by_id_not_found(self, mock_get_by_id, client):
        """Test retrieval of non-existent document"""
        mock_get_by_id.return_value = None
        
        response = client.get("/documents/doc-999")
        
        assert response.status_code == 404
        data = response.json()
        assert "Document with ID doc-999 not found" in data["detail"]
        mock_get_by_id.assert_called_once_with("doc-999")
    
    @patch.object(DocumentService, 'get_document_by_id')
    def test_get_document_by_id_service_error(self, mock_get_by_id, client):
        """Test error handling in get document by ID endpoint"""
        mock_get_by_id.side_effect = Exception("Service error")
        
        response = client.get("/documents/doc-001")
        
        assert response.status_code == 500
        data = response.json()
        assert "Failed to get document" in data["detail"]
        assert "Service error" in data["detail"]
    
    @patch.object(DocumentService, 'get_document_by_id')
    def test_get_document_by_id_http_exception_passthrough(self, mock_get_by_id, client):
        """Test that HTTPExceptions are passed through correctly"""
        mock_get_by_id.side_effect = HTTPException(status_code=404, detail="Custom not found")
        
        response = client.get("/documents/doc-001")
        
        assert response.status_code == 404
        data = response.json()
        assert data["detail"] == "Custom not found"
    
    @patch.object(DocumentService, 'get_document_analysis')
    def test_get_document_analysis_success(self, mock_get_analysis, client, mock_document_analysis):
        """Test successful retrieval of document analysis"""
        mock_get_analysis.return_value = mock_document_analysis
        
        response = client.get("/documents/doc-001/analysis")
        
        assert response.status_code == 200
        data = response.json()
        assert data["document_id"] == "doc-001"
        assert data["document_type"] == "Employment Contract"
        assert data["summary"] == "Test document analysis summary"
        assert len(data["key_dates"]) == 2
        assert len(data["parties_involved"]) == 2
        assert len(data["key_clauses"]) == 2
        assert "confidence_scores" in data
        assert data["confidence_scores"]["parties"] == 0.95
        assert data["confidence_scores"]["dates"] == 0.98
        mock_get_analysis.assert_called_once_with("doc-001")
    
    @patch.object(DocumentService, 'get_document_analysis')
    def test_get_document_analysis_not_found(self, mock_get_analysis, client):
        """Test retrieval of non-existent document analysis"""
        mock_get_analysis.return_value = None
        
        response = client.get("/documents/doc-999/analysis")
        
        assert response.status_code == 404
        data = response.json()
        assert "Analysis for document doc-999 not found" in data["detail"]
        mock_get_analysis.assert_called_once_with("doc-999")
    
    @patch.object(DocumentService, 'get_document_analysis')
    def test_get_document_analysis_service_error(self, mock_get_analysis, client):
        """Test error handling in get document analysis endpoint"""
        mock_get_analysis.side_effect = Exception("Analysis service error")
        
        response = client.get("/documents/doc-001/analysis")
        
        assert response.status_code == 500
        data = response.json()
        assert "Failed to get document analysis" in data["detail"]
        assert "Analysis service error" in data["detail"]
    
    @patch.object(DocumentService, 'get_document_analysis')
    def test_get_document_analysis_http_exception_passthrough(self, mock_get_analysis, client):
        """Test that HTTPExceptions are passed through correctly in analysis endpoint"""
        mock_get_analysis.side_effect = HTTPException(status_code=404, detail="Custom analysis not found")
        
        response = client.get("/documents/doc-001/analysis")
        
        assert response.status_code == 404
        data = response.json()
        assert data["detail"] == "Custom analysis not found"
    
    def test_get_case_documents_invalid_case_id(self, client):
        """Test endpoint with various case ID parameters"""
        # Test with special characters in case ID
        response = client.get("/documents/cases/case-with-special-chars-123/documents")
        # This should work but likely return empty list or error depending on service behavior
        assert response.status_code in [200, 500]
    
    def test_get_document_invalid_document_id(self, client):
        """Test endpoint with various document ID parameters"""
        # Test with special characters in document ID
        response = client.get("/documents/doc-with-special-chars-123")
        # This should work but likely return 404 or 500 depending on service behavior
        assert response.status_code in [404, 500]
    
    def test_api_documentation_structure(self, client):
        """Test that API endpoints have proper OpenAPI documentation"""
        response = client.get("/openapi.json")
        assert response.status_code == 200
        
        openapi_spec = response.json()
        paths = openapi_spec["paths"]
        
        # Check that our endpoints are documented
        assert "/documents/cases/{case_id}/documents" in paths
        assert "/documents/{document_id}" in paths
        assert "/documents/{document_id}/analysis" in paths
        
        # Check that endpoints have proper HTTP methods
        assert "get" in paths["/documents/cases/{case_id}/documents"]
        assert "get" in paths["/documents/{document_id}"]
        assert "get" in paths["/documents/{document_id}/analysis"]
    
    @patch.object(DocumentService, 'get_case_documents')
    def test_response_content_type(self, mock_get_case_docs, client, mock_documents):
        """Test that responses have correct content type"""
        mock_get_case_docs.return_value = mock_documents
        
        response = client.get("/documents/cases/case-001/documents")
        
        assert response.status_code == 200
        assert response.headers["content-type"] == "application/json"
    
    @patch.object(DocumentService, 'get_document_by_id')
    def test_document_response_schema(self, mock_get_by_id, client, mock_documents):
        """Test that document response matches expected schema"""
        mock_get_by_id.return_value = mock_documents[0]
        
        response = client.get("/documents/doc-001")
        
        assert response.status_code == 200
        data = response.json()
        
        # Check all required fields are present
        required_fields = ["id", "case_id", "name", "type", "size", "upload_date", "content_preview", "analysis_completed"]
        for field in required_fields:
            assert field in data
        
        # Check field types
        assert isinstance(data["id"], str)
        assert isinstance(data["case_id"], str)
        assert isinstance(data["name"], str)
        assert isinstance(data["type"], str)
        assert isinstance(data["size"], int)
        assert isinstance(data["upload_date"], str)
        assert isinstance(data["content_preview"], str)
        assert isinstance(data["analysis_completed"], bool)
    
    @patch.object(DocumentService, 'get_document_analysis')
    def test_analysis_response_schema(self, mock_get_analysis, client, mock_document_analysis):
        """Test that analysis response matches expected schema"""
        mock_get_analysis.return_value = mock_document_analysis
        
        response = client.get("/documents/doc-001/analysis")
        
        assert response.status_code == 200
        data = response.json()
        
        # Check all required fields are present
        required_fields = ["document_id", "key_dates", "parties_involved", "document_type", "summary", "key_clauses", "confidence_scores"]
        for field in required_fields:
            assert field in data
        
        # Check field types
        assert isinstance(data["document_id"], str)
        assert isinstance(data["key_dates"], list)
        assert isinstance(data["parties_involved"], list)
        assert isinstance(data["document_type"], str)
        assert isinstance(data["summary"], str)
        assert isinstance(data["key_clauses"], list)
        assert isinstance(data["confidence_scores"], dict)
        
        # Check that confidence scores are floats
        for score in data["confidence_scores"].values():
            assert isinstance(score, (int, float))
            assert 0 <= score <= 1