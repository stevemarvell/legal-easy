import pytest
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient
from datetime import datetime, date
from main import app
from app.services.document_service import DocumentService
from app.services.ai_analysis_service import AIAnalysisService
from app.models.document import Document, DocumentAnalysis


class TestAnalyzeEndpoint:
    """Test the new POST /documents/{id}/analyze endpoint"""
    
    @pytest.fixture
    def client(self):
        """Create a test client"""
        return TestClient(app)
    
    @pytest.fixture
    def sample_document(self):
        """Create a sample document for testing"""
        return Document(
            id="doc-001",
            case_id="case-001",
            name="Employment Contract - Sarah Chen",
            type="Contract",
            size=245760,
            upload_date=datetime(2024, 1, 15, 9, 30, 0),
            content_preview="EMPLOYMENT AGREEMENT between TechCorp Solutions Ltd. and Sarah Chen...",
            analysis_completed=True,
            full_content_path="backend/app/data/documents/case-001/employment_contract_sarah_chen.txt"
        )
    
    @pytest.fixture
    def sample_analysis(self):
        """Create a sample document analysis for testing"""
        return DocumentAnalysis(
            document_id="doc-001",
            key_dates=[date(2022, 3, 15), date(2024, 1, 12)],
            parties_involved=["Sarah Chen", "TechCorp Solutions Ltd."],
            document_type="Employment Contract",
            summary="Employment agreement for Senior Safety Engineer position...",
            key_clauses=["Notice period requirements", "Compensation provisions"],
            confidence_scores={"parties": 0.95, "dates": 0.98, "contract_terms": 0.92}
        )
    
    @patch.object(DocumentService, 'get_document_by_id')
    @patch.object(AIAnalysisService, 'analyze_document')
    def test_analyze_document_success(self, mock_analyze, mock_get_doc, client, sample_document, sample_analysis):
        """Test successful document analysis"""
        mock_get_doc.return_value = sample_document
        mock_analyze.return_value = sample_analysis
        
        response = client.post("/api/documents/doc-001/analyze")
        
        assert response.status_code == 200
        data = response.json()
        assert data["document_id"] == "doc-001"
        assert data["document_type"] == "Employment Contract"
        assert len(data["parties_involved"]) == 2
        assert len(data["key_dates"]) == 2
        assert "confidence_scores" in data
        
        mock_get_doc.assert_called_once_with("doc-001")
        mock_analyze.assert_called_once_with(sample_document)
    
    @patch.object(DocumentService, 'get_document_by_id')
    def test_analyze_document_not_found(self, mock_get_doc, client):
        """Test analysis of non-existent document"""
        mock_get_doc.return_value = None
        
        response = client.post("/api/documents/doc-999/analyze")
        
        assert response.status_code == 404
        data = response.json()
        assert "Document with ID doc-999 not found" in data["detail"]
        
        mock_get_doc.assert_called_once_with("doc-999")
    
    @patch.object(DocumentService, 'get_document_by_id')
    def test_analyze_document_service_error(self, mock_get_doc, client):
        """Test error handling when document service fails"""
        mock_get_doc.side_effect = Exception("Service error")
        
        response = client.post("/api/documents/doc-001/analyze")
        
        assert response.status_code == 500
        data = response.json()
        assert "Failed to analyze document" in data["detail"]
    
    @patch.object(DocumentService, 'get_document_by_id')
    @patch.object(AIAnalysisService, 'analyze_document')
    def test_analyze_document_analysis_error(self, mock_analyze, mock_get_doc, client, sample_document):
        """Test error handling when AI analysis fails"""
        mock_get_doc.return_value = sample_document
        mock_analyze.side_effect = Exception("Analysis failed")
        
        response = client.post("/api/documents/doc-001/analyze")
        
        assert response.status_code == 500
        data = response.json()
        assert "Failed to analyze document" in data["detail"]
    
    @patch.object(DocumentService, 'get_document_by_id')
    @patch.object(AIAnalysisService, 'analyze_document')
    def test_analyze_document_response_schema(self, mock_analyze, mock_get_doc, client, sample_document, sample_analysis):
        """Test that the response matches the expected schema"""
        mock_get_doc.return_value = sample_document
        mock_analyze.return_value = sample_analysis
        
        response = client.post("/api/documents/doc-001/analyze")
        
        assert response.status_code == 200
        data = response.json()
        
        # Check required fields
        required_fields = ["document_id", "key_dates", "parties_involved", "document_type", 
                          "summary", "key_clauses", "confidence_scores"]
        for field in required_fields:
            assert field in data
        
        # Check data types
        assert isinstance(data["key_dates"], list)
        assert isinstance(data["parties_involved"], list)
        assert isinstance(data["document_type"], str)
        assert isinstance(data["summary"], str)
        assert isinstance(data["key_clauses"], list)
        assert isinstance(data["confidence_scores"], dict)
    
    def test_analyze_endpoint_documentation(self, client):
        """Test that the analyze endpoint is properly documented in OpenAPI"""
        response = client.get("/openapi.json")
        assert response.status_code == 200
        
        openapi_spec = response.json()
        paths = openapi_spec["paths"]
        
        # Check that our new endpoint is documented
        assert "/api/documents/{document_id}/analyze" in paths
        analyze_endpoint = paths["/api/documents/{document_id}/analyze"]
        assert "post" in analyze_endpoint
        
        post_spec = analyze_endpoint["post"]
        assert "summary" in post_spec
        assert "description" in post_spec
        assert "responses" in post_spec
        assert "200" in post_spec["responses"]
        assert "404" in post_spec["responses"]
        assert "500" in post_spec["responses"]
    
    @patch.object(DocumentService, 'get_document_by_id')
    @patch.object(AIAnalysisService, 'analyze_document')
    def test_analyze_endpoint_content_type(self, mock_analyze, mock_get_doc, client, sample_document, sample_analysis):
        """Test that the response has correct content type"""
        mock_get_doc.return_value = sample_document
        mock_analyze.return_value = sample_analysis
        
        response = client.post("/api/documents/doc-001/analyze")
        
        assert response.status_code == 200
        assert response.headers["content-type"] == "application/json"
    
    @patch.object(DocumentService, 'get_document_by_id')
    @patch.object(AIAnalysisService, 'analyze_document')
    def test_analyze_different_document_types(self, mock_analyze, mock_get_doc, client):
        """Test analysis with different document types"""
        document_types = ["Contract", "Email", "Evidence", "Legal Brief"]
        
        for doc_type in document_types:
            doc_id = f"doc-{doc_type.lower()}"
            test_document = Document(
                id=doc_id,
                case_id="case-001",
                name=f"Test {doc_type}",
                type=doc_type,
                size=1024,
                upload_date=datetime(2024, 1, 15, 9, 30, 0),
                content_preview=f"This is a test {doc_type.lower()}...",
                analysis_completed=False
            )
            
            # Create analysis with matching document ID
            test_analysis = DocumentAnalysis(
                document_id=doc_id,
                key_dates=[date(2022, 3, 15)],
                parties_involved=["Test Party"],
                document_type=doc_type,
                summary=f"Test {doc_type.lower()} analysis",
                key_clauses=[f"Test {doc_type.lower()} clause"],
                confidence_scores={"parties": 0.9, "dates": 0.9}
            )
            
            mock_get_doc.return_value = test_document
            mock_analyze.return_value = test_analysis
            
            response = client.post(f"/api/documents/{doc_id}/analyze")
            
            assert response.status_code == 200
            data = response.json()
            assert data["document_id"] == doc_id
            assert data["document_type"] == doc_type