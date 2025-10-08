import pytest
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient
from fastapi import HTTPException

from main import app
from app.models.playbook import Playbook, PlaybookRule, PlaybookResult, MonetaryRange
from app.models.case import Case
from app.services.playbook_engine import PlaybookEngine
from app.services.case_service import CaseService


class TestPlaybooksAPI:
    """Test suite for playbook API endpoints"""
    
    @pytest.fixture
    def client(self):
        """Create test client"""
        return TestClient(app)
    
    @pytest.fixture
    def mock_playbook(self):
        """Create mock playbook for testing"""
        return Playbook(
            id="employment-dispute",
            case_type="Employment Dispute",
            name="Employment Law Playbook",
            rules=[
                PlaybookRule(
                    id="rule-001",
                    condition="termination_within_protected_period",
                    action="investigate_retaliation_claim",
                    weight=0.9,
                    description="Test rule description"
                )
            ],
            decision_tree={"root": "test"},
            monetary_ranges={
                "high": MonetaryRange(
                    range=[200000, 1000000],
                    description="High damages",
                    factors=["Full compensatory damages"]
                )
            },
            escalation_paths=["Internal HR complaint"]
        )
    
    @pytest.fixture
    def mock_playbooks(self, mock_playbook):
        """Create list of mock playbooks"""
        contract_playbook = Playbook(
            id="contract-breach",
            case_type="Contract Breach",
            name="Contract Breach Playbook",
            rules=[],
            decision_tree={},
            monetary_ranges={},
            escalation_paths=[]
        )
        return [mock_playbook, contract_playbook]
    
    @pytest.fixture
    def mock_case(self):
        """Create mock case for testing"""
        from datetime import datetime
        return Case(
            id="case-001",
            title="Test Case",
            case_type="Employment Dispute",
            client_name="Test Client",
            status="Active",
            created_date=datetime.now(),
            summary="Test case summary",
            key_parties=["Party 1"],
            documents=["doc-001"],
            playbook_id="employment-dispute"
        )
    
    @pytest.fixture
    def mock_playbook_result(self):
        """Create mock playbook result"""
        return PlaybookResult(
            case_id="case-001",
            playbook_id="employment-dispute",
            applied_rules=["rule-001"],
            recommendations=["investigate_retaliation_claim"],
            case_strength="Strong",
            reasoning="Test reasoning"
        )

    # Test GET /playbooks
    @patch.object(PlaybookEngine, 'get_all_playbooks')
    def test_get_all_playbooks_success(self, mock_get_all, client, mock_playbooks):
        """Test successful retrieval of all playbooks"""
        mock_get_all.return_value = mock_playbooks
        
        response = client.get("/playbooks/")
        
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2
        assert data[0]["case_type"] == "Employment Dispute"
        assert data[1]["case_type"] == "Contract Breach"
        mock_get_all.assert_called_once()

    @patch.object(PlaybookEngine, 'get_all_playbooks')
    def test_get_all_playbooks_empty_list(self, mock_get_all, client):
        """Test retrieval when no playbooks exist"""
        mock_get_all.return_value = []
        
        response = client.get("/playbooks/")
        
        assert response.status_code == 200
        data = response.json()
        assert data == []
        mock_get_all.assert_called_once()

    @patch.object(PlaybookEngine, 'get_all_playbooks')
    def test_get_all_playbooks_error(self, mock_get_all, client):
        """Test error handling when getting all playbooks fails"""
        mock_get_all.side_effect = Exception("Database error")
        
        response = client.get("/playbooks/")
        
        assert response.status_code == 500
        data = response.json()
        assert "Failed to get playbooks" in data["detail"]

    # Test GET /playbooks/{case_type}
    @patch.object(PlaybookEngine, 'get_playbook_by_case_type')
    def test_get_playbook_success(self, mock_get_playbook, client, mock_playbook):
        """Test successful retrieval of playbook by case type"""
        mock_get_playbook.return_value = mock_playbook
        
        response = client.get("/playbooks/Employment Dispute")
        
        assert response.status_code == 200
        data = response.json()
        assert data["case_type"] == "Employment Dispute"
        assert data["name"] == "Employment Law Playbook"
        assert len(data["rules"]) == 1
        mock_get_playbook.assert_called_once_with("Employment Dispute")

    @patch.object(PlaybookEngine, 'get_playbook_by_case_type')
    def test_get_playbook_not_found(self, mock_get_playbook, client):
        """Test playbook not found scenario"""
        mock_get_playbook.return_value = None
        
        response = client.get("/playbooks/Unknown Type")
        
        assert response.status_code == 404
        data = response.json()
        assert "No playbook found for case type: Unknown Type" in data["detail"]
        mock_get_playbook.assert_called_once_with("Unknown Type")

    @patch.object(PlaybookEngine, 'get_playbook_by_case_type')
    def test_get_playbook_service_error(self, mock_get_playbook, client):
        """Test error handling when getting playbook fails"""
        mock_get_playbook.side_effect = Exception("Service error")
        
        response = client.get("/playbooks/Employment Dispute")
        
        assert response.status_code == 500
        data = response.json()
        assert "Failed to get playbook" in data["detail"]

    # Test GET /playbooks/cases/{case_id}/applied-rules
    @patch.object(CaseService, 'get_case_by_id')
    @patch.object(PlaybookEngine, 'get_playbook_by_case_type')
    @patch.object(PlaybookEngine, 'apply_playbook_rules')
    def test_get_applied_rules_success(self, mock_apply_rules, mock_get_playbook, 
                                     mock_get_case, client, mock_case, mock_playbook, 
                                     mock_playbook_result):
        """Test successful retrieval of applied rules"""
        mock_get_case.return_value = mock_case
        mock_get_playbook.return_value = mock_playbook
        mock_apply_rules.return_value = mock_playbook_result
        
        response = client.get("/playbooks/cases/case-001/applied-rules")
        
        assert response.status_code == 200
        data = response.json()
        assert data["case_id"] == "case-001"
        assert data["playbook_id"] == "employment-dispute"
        assert data["case_strength"] == "Strong"
        assert len(data["applied_rules"]) == 1
        
        mock_get_case.assert_called_once_with("case-001")
        mock_get_playbook.assert_called_once_with("Employment Dispute")
        mock_apply_rules.assert_called_once_with(mock_case, mock_playbook)

    @patch.object(CaseService, 'get_case_by_id')
    def test_get_applied_rules_case_not_found(self, mock_get_case, client):
        """Test applied rules when case is not found"""
        mock_get_case.return_value = None
        
        response = client.get("/playbooks/cases/case-999/applied-rules")
        
        assert response.status_code == 404
        data = response.json()
        assert "Case with ID case-999 not found" in data["detail"]
        mock_get_case.assert_called_once_with("case-999")

    @patch.object(CaseService, 'get_case_by_id')
    @patch.object(PlaybookEngine, 'get_playbook_by_case_type')
    def test_get_applied_rules_no_playbook(self, mock_get_playbook, mock_get_case, 
                                         client, mock_case):
        """Test applied rules when no playbook is available"""
        mock_get_case.return_value = mock_case
        mock_get_playbook.return_value = None
        
        response = client.get("/playbooks/cases/case-001/applied-rules")
        
        assert response.status_code == 404
        data = response.json()
        assert "No playbook available for case type: Employment Dispute" in data["detail"]

    @patch.object(CaseService, 'get_case_by_id')
    def test_get_applied_rules_case_service_error(self, mock_get_case, client):
        """Test error handling when case service fails"""
        mock_get_case.side_effect = Exception("Case service error")
        
        response = client.get("/playbooks/cases/case-001/applied-rules")
        
        assert response.status_code == 500
        data = response.json()
        assert "Failed to get applied rules" in data["detail"]

    @patch.object(CaseService, 'get_case_by_id')
    @patch.object(PlaybookEngine, 'get_playbook_by_case_type')
    @patch.object(PlaybookEngine, 'apply_playbook_rules')
    def test_get_applied_rules_playbook_engine_error(self, mock_apply_rules, 
                                                   mock_get_playbook, mock_get_case, 
                                                   client, mock_case, mock_playbook):
        """Test error handling when playbook engine fails"""
        mock_get_case.return_value = mock_case
        mock_get_playbook.return_value = mock_playbook
        mock_apply_rules.side_effect = Exception("Playbook engine error")
        
        response = client.get("/playbooks/cases/case-001/applied-rules")
        
        assert response.status_code == 500
        data = response.json()
        assert "Failed to get applied rules" in data["detail"]

    # Test HTTP exception passthrough
    @patch.object(PlaybookEngine, 'get_playbook_by_case_type')
    def test_get_playbook_http_exception_passthrough(self, mock_get_playbook, client):
        """Test that HTTPExceptions are passed through correctly"""
        mock_get_playbook.side_effect = HTTPException(status_code=403, detail="Forbidden")
        
        response = client.get("/playbooks/Employment Dispute")
        
        assert response.status_code == 403
        data = response.json()
        assert data["detail"] == "Forbidden"

    # Test API documentation and response structure
    def test_api_documentation_structure(self, client):
        """Test that API endpoints have proper documentation"""
        response = client.get("/openapi.json")
        assert response.status_code == 200
        
        openapi_spec = response.json()
        paths = openapi_spec["paths"]
        
        # Check that playbook endpoints are documented
        assert "/playbooks/" in paths
        assert "/playbooks/{case_type}" in paths
        assert "/playbooks/cases/{case_id}/applied-rules" in paths
        
        # Check that endpoints have proper descriptions
        get_all_endpoint = paths["/playbooks/"]["get"]
        assert "summary" in get_all_endpoint
        assert "description" in get_all_endpoint

    def test_response_content_type(self, client):
        """Test that responses have correct content type"""
        with patch.object(PlaybookEngine, 'get_all_playbooks', return_value=[]):
            response = client.get("/playbooks/")
            assert response.headers["content-type"] == "application/json"

    @patch.object(PlaybookEngine, 'get_all_playbooks')
    def test_playbook_response_schema(self, mock_get_all, client, mock_playbooks):
        """Test that playbook responses match expected schema"""
        mock_get_all.return_value = mock_playbooks
        
        response = client.get("/playbooks/")
        assert response.status_code == 200
        
        data = response.json()
        playbook = data[0]
        
        # Check required fields
        required_fields = ["id", "case_type", "name", "rules", "decision_tree", 
                          "monetary_ranges", "escalation_paths"]
        for field in required_fields:
            assert field in playbook
        
        # Check rule structure
        if playbook["rules"]:
            rule = playbook["rules"][0]
            rule_fields = ["id", "condition", "action", "weight", "description"]
            for field in rule_fields:
                assert field in rule

    @patch.object(CaseService, 'get_case_by_id')
    @patch.object(PlaybookEngine, 'get_playbook_by_case_type')
    @patch.object(PlaybookEngine, 'apply_playbook_rules')
    def test_applied_rules_response_schema(self, mock_apply_rules, mock_get_playbook, 
                                         mock_get_case, client, mock_case, mock_playbook, 
                                         mock_playbook_result):
        """Test that applied rules responses match expected schema"""
        mock_get_case.return_value = mock_case
        mock_get_playbook.return_value = mock_playbook
        mock_apply_rules.return_value = mock_playbook_result
        
        response = client.get("/playbooks/cases/case-001/applied-rules")
        assert response.status_code == 200
        
        data = response.json()
        
        # Check required fields
        required_fields = ["case_id", "playbook_id", "applied_rules", 
                          "recommendations", "case_strength", "reasoning"]
        for field in required_fields:
            assert field in data
        
        # Check data types
        assert isinstance(data["applied_rules"], list)
        assert isinstance(data["recommendations"], list)
        assert isinstance(data["case_strength"], str)
        assert isinstance(data["reasoning"], str)

    # Test edge cases
    def test_get_playbook_with_special_characters(self, client):
        """Test playbook retrieval with special characters in case type"""
        with patch.object(PlaybookEngine, 'get_playbook_by_case_type', return_value=None):
            response = client.get("/playbooks/Contract%20Breach%20%26%20Dispute")
            assert response.status_code == 404

    def test_get_applied_rules_with_special_case_id(self, client):
        """Test applied rules with special characters in case ID"""
        with patch.object(CaseService, 'get_case_by_id', return_value=None):
            response = client.get("/playbooks/cases/case-001%20test/applied-rules")
            assert response.status_code == 404

    @patch.object(PlaybookEngine, 'get_all_playbooks')
    def test_get_all_playbooks_large_dataset(self, mock_get_all, client):
        """Test performance with large number of playbooks"""
        # Create many mock playbooks
        large_playbook_list = []
        for i in range(100):
            playbook = Playbook(
                id=f"playbook-{i}",
                case_type=f"Case Type {i}",
                name=f"Playbook {i}",
                rules=[],
                decision_tree={},
                monetary_ranges={},
                escalation_paths=[]
            )
            large_playbook_list.append(playbook)
        
        mock_get_all.return_value = large_playbook_list
        
        response = client.get("/playbooks/")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 100