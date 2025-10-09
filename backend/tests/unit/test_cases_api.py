import pytest
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient
from fastapi import HTTPException
from datetime import datetime
from main import app
from app.models.case import Case, CaseStatistics
from app.models.playbook import CaseAssessment
from app.services.case_service import CaseService
from app.services.playbook_engine import PlaybookEngine


class TestCasesAPI:
    """Test the Cases API endpoints"""
    
    @pytest.fixture
    def client(self):
        """Create a test client for the FastAPI app"""
        return TestClient(app)
    
    @pytest.fixture
    def mock_cases(self):
        """Mock cases data for testing"""
        return [
            Case(
                id="case-001",
                title="Test Case 1",
                case_type="Employment Dispute",
                client_name="John Doe",
                status="Active",
                created_date=datetime(2024, 1, 15, 9, 0, 0),
                summary="Test case summary",
                key_parties=["John Doe", "Company Inc"],
                documents=["doc-001", "doc-002"],
                playbook_id="employment-dispute"
            ),
            Case(
                id="case-002",
                title="Test Case 2",
                case_type="Contract Breach",
                client_name="Jane Smith",
                status="Under Review",
                created_date=datetime(2024, 2, 1, 10, 0, 0),
                summary="Another test case",
                key_parties=["Jane Smith", "Vendor LLC"],
                documents=["doc-003"],
                playbook_id="contract-breach"
            )
        ]
    
    @pytest.fixture
    def mock_case_statistics(self):
        """Mock case statistics for testing"""
        return CaseStatistics(
            total_cases=6,
            active_cases=3,
            resolved_cases=1,
            under_review_cases=2,
            recent_activity_count=4
        )
    
    @patch.object(CaseService, 'get_case_statistics')
    def test_get_case_statistics_success(self, mock_get_stats, client, mock_case_statistics):
        """Test successful retrieval of case statistics"""
        mock_get_stats.return_value = mock_case_statistics
        
        response = client.get("/api/cases/statistics")
        
        assert response.status_code == 200
        data = response.json()
        assert data["total_cases"] == 6
        assert data["active_cases"] == 3
        assert data["resolved_cases"] == 1
        assert data["under_review_cases"] == 2
        assert data["recent_activity_count"] == 4
        mock_get_stats.assert_called_once()
    
    @patch.object(CaseService, 'get_case_statistics')
    def test_get_case_statistics_error(self, mock_get_stats, client):
        """Test error handling in case statistics endpoint"""
        mock_get_stats.side_effect = Exception("Database error")
        
        response = client.get("/api/cases/statistics")
        
        assert response.status_code == 500
        data = response.json()
        assert "Failed to get case statistics" in data["detail"]
        assert "Database error" in data["detail"]
    
    @patch.object(CaseService, 'get_all_cases')
    def test_get_cases_success(self, mock_get_all, client, mock_cases):
        """Test successful retrieval of all cases"""
        mock_get_all.return_value = mock_cases
        
        response = client.get("/api/cases/")
        
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2
        assert data[0]["id"] == "case-001"
        assert data[0]["title"] == "Test Case 1"
        assert data[0]["case_type"] == "Employment Dispute"
        assert data[1]["id"] == "case-002"
        assert data[1]["client_name"] == "Jane Smith"
        mock_get_all.assert_called_once()
    
    @patch.object(CaseService, 'get_all_cases')
    def test_get_cases_empty_list(self, mock_get_all, client):
        """Test retrieval when no cases exist"""
        mock_get_all.return_value = []
        
        response = client.get("/api/cases/")
        
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 0
        assert data == []
    
    @patch.object(CaseService, 'get_all_cases')
    def test_get_cases_error(self, mock_get_all, client):
        """Test error handling in get all cases endpoint"""
        mock_get_all.side_effect = Exception("Service error")
        
        response = client.get("/api/cases/")
        
        assert response.status_code == 500
        data = response.json()
        assert "Failed to get cases" in data["detail"]
        assert "Service error" in data["detail"]
    
    @patch.object(CaseService, 'get_case_by_id')
    def test_get_case_by_id_success(self, mock_get_by_id, client, mock_cases):
        """Test successful retrieval of a specific case"""
        mock_get_by_id.return_value = mock_cases[0]
        
        response = client.get("/api/cases/case-001")
        
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == "case-001"
        assert data["title"] == "Test Case 1"
        assert data["case_type"] == "Employment Dispute"
        assert data["client_name"] == "John Doe"
        assert data["status"] == "Active"
        assert len(data["key_parties"]) == 2
        assert len(data["documents"]) == 2
        mock_get_by_id.assert_called_once_with("case-001")
    
    @patch.object(CaseService, 'get_case_by_id')
    def test_get_case_by_id_not_found(self, mock_get_by_id, client):
        """Test retrieval of non-existent case"""
        mock_get_by_id.return_value = None
        
        response = client.get("/api/cases/case-999")
        
        assert response.status_code == 404
        data = response.json()
        assert "Case with ID case-999 not found" in data["detail"]
        mock_get_by_id.assert_called_once_with("case-999")
    
    @patch.object(CaseService, 'get_case_by_id')
    def test_get_case_by_id_service_error(self, mock_get_by_id, client):
        """Test error handling in get case by ID endpoint"""
        mock_get_by_id.side_effect = Exception("Service error")
        
        response = client.get("/api/cases/case-001")
        
        assert response.status_code == 500
        data = response.json()
        assert "Failed to get case" in data["detail"]
        assert "Service error" in data["detail"]
    
    @patch.object(CaseService, 'get_case_by_id')
    def test_get_case_by_id_http_exception_passthrough(self, mock_get_by_id, client):
        """Test that HTTPExceptions are passed through correctly"""
        mock_get_by_id.side_effect = HTTPException(status_code=404, detail="Custom not found")
        
        response = client.get("/api/cases/case-001")
        
        assert response.status_code == 404
        data = response.json()
        assert data["detail"] == "Custom not found"
    
    def test_get_case_invalid_path_parameter(self, client):
        """Test endpoint with various path parameters"""
        # Test with empty case ID (should still work as it's a valid string)
        response = client.get("/api/cases/")
        assert response.status_code == 200  # This hits the get_cases endpoint
        
        # Test with special characters in case ID
        response = client.get("/api/cases/case-with-special-chars-123")
        # This should work but likely return 404 or 500 depending on service behavior
        assert response.status_code in [404, 500]
    
    def test_api_documentation_structure(self, client):
        """Test that API endpoints have proper OpenAPI documentation"""
        response = client.get("/openapi.json")
        assert response.status_code == 200
        
        openapi_spec = response.json()
        paths = openapi_spec["paths"]
        
        # Check that our endpoints are documented
        assert "/api/cases/" in paths
        assert "/api/cases/{case_id}" in paths
        assert "/api/cases/statistics" in paths
        
        # Check that endpoints have proper HTTP methods
        assert "get" in paths["/api/cases/"]
        assert "get" in paths["/api/cases/{case_id}"]
        assert "get" in paths["/api/cases/statistics"]
    
    @patch.object(CaseService, 'get_all_cases')
    def test_response_content_type(self, mock_get_all, client, mock_cases):
        """Test that responses have correct content type"""
        mock_get_all.return_value = mock_cases
        
        response = client.get("/api/cases/")
        
        assert response.status_code == 200
        assert response.headers["content-type"] == "application/json"
    
    @patch.object(CaseService, 'get_case_statistics')
    def test_statistics_response_schema(self, mock_get_stats, client, mock_case_statistics):
        """Test that statistics response matches expected schema"""
        mock_get_stats.return_value = mock_case_statistics
        
        response = client.get("/api/cases/statistics")
        
        assert response.status_code == 200
        data = response.json()
        
        # Check all required fields are present
        required_fields = ["total_cases", "active_cases", "resolved_cases", "under_review_cases", "recent_activity_count"]
        for field in required_fields:
            assert field in data
            assert isinstance(data[field], int)
            assert data[field] >= 0
    
    @pytest.fixture
    def mock_case_assessment(self):
        """Mock case assessment for testing"""
        return CaseAssessment(
            case_id="case-001",
            playbook_used="Employment Law Playbook",
            case_strength="Strong",
            key_issues=["Wrongful termination claim", "Retaliation for protected activity"],
            recommended_actions=["investigate_retaliation_claim", "document_harassment_incidents"],
            monetary_assessment=(200000, 1000000),
            applied_rules=["rule-001", "rule-004"],
            reasoning="Case shows strong prospects based on 2 applicable rules. Key factors support the client's position in this employment dispute matter."
        )
    
    @patch.object(CaseService, 'get_case_by_id')
    @patch.object(PlaybookEngine, 'generate_case_assessment')
    def test_get_case_assessment_success(self, mock_generate_assessment, mock_get_case, client, mock_cases, mock_case_assessment):
        """Test successful generation of case assessment"""
        mock_get_case.return_value = mock_cases[0]
        mock_generate_assessment.return_value = mock_case_assessment
        
        response = client.get("/api/cases/case-001/assessment")
        
        assert response.status_code == 200
        data = response.json()
        assert data["case_id"] == "case-001"
        assert data["playbook_used"] == "Employment Law Playbook"
        assert data["case_strength"] == "Strong"
        assert len(data["key_issues"]) == 2
        assert len(data["recommended_actions"]) == 2
        assert len(data["applied_rules"]) == 2
        assert data["monetary_assessment"] == [200000, 1000000]
        assert "strong prospects" in data["reasoning"]
        
        mock_get_case.assert_called_once_with("case-001")
        mock_generate_assessment.assert_called_once_with(mock_cases[0])
    
    @patch.object(CaseService, 'get_case_by_id')
    def test_get_case_assessment_case_not_found(self, mock_get_case, client):
        """Test case assessment when case doesn't exist"""
        mock_get_case.return_value = None
        
        response = client.get("/api/cases/case-999/assessment")
        
        assert response.status_code == 404
        data = response.json()
        assert "Case with ID case-999 not found" in data["detail"]
        mock_get_case.assert_called_once_with("case-999")
    
    @patch.object(CaseService, 'get_case_by_id')
    @patch.object(PlaybookEngine, 'generate_case_assessment')
    def test_get_case_assessment_no_playbook(self, mock_generate_assessment, mock_get_case, client, mock_cases):
        """Test case assessment when no playbook is available"""
        mock_get_case.return_value = mock_cases[0]
        mock_generate_assessment.return_value = None
        
        response = client.get("/api/cases/case-001/assessment")
        
        assert response.status_code == 404
        data = response.json()
        assert "No playbook available for case type: Employment Dispute" in data["detail"]
        mock_get_case.assert_called_once_with("case-001")
        mock_generate_assessment.assert_called_once_with(mock_cases[0])
    
    @patch.object(CaseService, 'get_case_by_id')
    @patch.object(PlaybookEngine, 'generate_case_assessment')
    def test_get_case_assessment_service_error(self, mock_generate_assessment, mock_get_case, client, mock_cases):
        """Test error handling in case assessment endpoint"""
        mock_get_case.return_value = mock_cases[0]
        mock_generate_assessment.side_effect = Exception("Playbook engine error")
        
        response = client.get("/api/cases/case-001/assessment")
        
        assert response.status_code == 500
        data = response.json()
        assert "Failed to generate case assessment" in data["detail"]
        assert "Playbook engine error" in data["detail"]
    
    @patch.object(CaseService, 'get_case_by_id')
    def test_get_case_assessment_case_service_error(self, mock_get_case, client):
        """Test error handling when case service fails"""
        mock_get_case.side_effect = Exception("Case service error")
        
        response = client.get("/api/cases/case-001/assessment")
        
        assert response.status_code == 500
        data = response.json()
        assert "Failed to generate case assessment" in data["detail"]
        assert "Case service error" in data["detail"]
    
    @patch.object(CaseService, 'get_case_by_id')
    @patch.object(PlaybookEngine, 'generate_case_assessment')
    def test_get_case_assessment_response_schema(self, mock_generate_assessment, mock_get_case, client, mock_cases, mock_case_assessment):
        """Test that case assessment response matches expected schema"""
        mock_get_case.return_value = mock_cases[0]
        mock_generate_assessment.return_value = mock_case_assessment
        
        response = client.get("/api/cases/case-001/assessment")
        
        assert response.status_code == 200
        data = response.json()
        
        # Check all required fields are present
        required_fields = ["case_id", "playbook_used", "case_strength", "key_issues", 
                          "recommended_actions", "monetary_assessment", "applied_rules", "reasoning"]
        for field in required_fields:
            assert field in data
        
        # Check field types
        assert isinstance(data["case_id"], str)
        assert isinstance(data["playbook_used"], str)
        assert data["case_strength"] in ["Strong", "Moderate", "Weak"]
        assert isinstance(data["key_issues"], list)
        assert isinstance(data["recommended_actions"], list)
        assert isinstance(data["applied_rules"], list)
        assert isinstance(data["reasoning"], str)
        
        # Check monetary assessment format
        if data["monetary_assessment"] is not None:
            assert isinstance(data["monetary_assessment"], list)
            assert len(data["monetary_assessment"]) == 2
            assert all(isinstance(x, int) for x in data["monetary_assessment"])
            assert data["monetary_assessment"][0] <= data["monetary_assessment"][1]