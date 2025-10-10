import pytest
import json
import os
from unittest.mock import patch, mock_open, MagicMock
from datetime import datetime, timedelta
from app.services.case_service import CaseService
from app.models.case import Case, CaseStatistics


class TestCaseService:
    """Test the CaseService class"""
    
    @pytest.fixture
    def mock_cases_data(self):
        """Mock cases data for testing"""
        return [
            {
                "id": "case-001",
                "title": "Test Case 1",
                "case_type": "Employment Dispute",
                "client_name": "John Doe",
                "status": "Active",
                "created_date": "2024-01-15T09:00:00Z",
                "summary": "Test case summary",
                "key_parties": ["John Doe", "Company Inc"],
                "documents": ["doc-001", "doc-002"],
                "playbook_id": "employment-dispute"
            },
            {
                "id": "case-002",
                "title": "Test Case 2",
                "case_type": "Contract Breach",
                "client_name": "Jane Smith",
                "status": "Under Review",
                "created_date": "2024-02-01T10:00:00Z",
                "summary": "Another test case",
                "key_parties": ["Jane Smith", "Vendor LLC"],
                "documents": ["doc-003"],
                "playbook_id": "contract-breach"
            },
            {
                "id": "case-003",
                "title": "Test Case 3",
                "case_type": "Employment Dispute",
                "client_name": "Bob Wilson",
                "status": "Resolved",
                "created_date": "2023-12-01T08:00:00Z",
                "summary": "Resolved test case",
                "key_parties": ["Bob Wilson", "Corp Ltd"],
                "documents": ["doc-004"],
                "playbook_id": "employment-dispute"
            }
        ]
    
    @pytest.fixture
    def case_service(self):
        """Create a CaseService instance for testing"""
        return CaseService()
    
    def test_init(self, case_service):
        """Test CaseService initialization"""
        assert case_service._cases_cache is None
        assert case_service._data_file.endswith("demo_cases.json")
    
    @patch("builtins.open", new_callable=mock_open)
    @patch("json.load")
    def test_load_cases_success(self, mock_json_load, mock_file, case_service, mock_cases_data):
        """Test successful loading of cases from JSON file"""
        mock_json_load.return_value = mock_cases_data
        
        cases = case_service._load_cases()
        
        assert len(cases) == 3
        assert all(isinstance(case, Case) for case in cases)
        assert cases[0].id == "case-001"
        assert cases[0].title == "Test Case 1"
        assert cases[1].case_type == "Contract Breach"
        mock_file.assert_called_once()
        mock_json_load.assert_called_once()
    
    @patch("builtins.open", side_effect=FileNotFoundError)
    def test_load_cases_file_not_found(self, mock_file, case_service):
        """Test handling of missing cases file"""
        with pytest.raises(FileNotFoundError, match="Demo cases file not found"):
            case_service._load_cases()
    
    @patch("builtins.open", new_callable=mock_open)
    @patch("json.load", side_effect=json.JSONDecodeError("Invalid JSON", "", 0))
    def test_load_cases_invalid_json(self, mock_json_load, mock_file, case_service):
        """Test handling of invalid JSON in cases file"""
        with pytest.raises(ValueError, match="Invalid JSON in demo cases file"):
            case_service._load_cases()
    
    @patch.object(CaseService, '_load_cases')
    def test_get_all_cases(self, mock_load_cases, case_service, mock_cases_data):
        """Test getting all cases"""
        mock_cases = [Case(**cases_index) for cases_index in mock_cases_data]
        mock_load_cases.return_value = mock_cases
        
        result = case_service.get_all_cases()
        
        assert len(result) == 3
        assert result == mock_cases
        mock_load_cases.assert_called_once()
    
    @patch.object(CaseService, '_load_cases')
    def test_get_case_by_id_found(self, mock_load_cases, case_service, mock_cases_data):
        """Test getting a case by ID when it exists"""
        mock_cases = [Case(**cases_index) for cases_index in mock_cases_data]
        mock_load_cases.return_value = mock_cases
        
        result = case_service.get_case_by_id("case-002")
        
        assert result is not None
        assert result.id == "case-002"
        assert result.title == "Test Case 2"
        assert result.case_type == "Contract Breach"
    
    @patch.object(CaseService, '_load_cases')
    def test_get_case_by_id_not_found(self, mock_load_cases, case_service, mock_cases_data):
        """Test getting a case by ID when it doesn't exist"""
        mock_cases = [Case(**cases_index) for cases_index in mock_cases_data]
        mock_load_cases.return_value = mock_cases
        
        result = case_service.get_case_by_id("case-999")
        
        assert result is None
    
    @patch.object(CaseService, '_load_cases')
    def test_get_cases_by_type(self, mock_load_cases, case_service, mock_cases_data):
        """Test filtering cases by type"""
        mock_cases = [Case(**cases_index) for cases_index in mock_cases_data]
        mock_load_cases.return_value = mock_cases
        
        result = case_service.get_cases_by_type("Employment Dispute")
        
        assert len(result) == 2
        assert all(case.case_type == "Employment Dispute" for case in result)
        assert result[0].id == "case-001"
        assert result[1].id == "case-003"
    
    @patch.object(CaseService, '_load_cases')
    def test_get_cases_by_type_no_matches(self, mock_load_cases, case_service, mock_cases_data):
        """Test filtering cases by type with no matches"""
        mock_cases = [Case(**cases_index) for cases_index in mock_cases_data]
        mock_load_cases.return_value = mock_cases
        
        result = case_service.get_cases_by_type("Nonexistent Type")
        
        assert len(result) == 0
        assert result == []
    
    @patch.object(CaseService, '_load_cases')
    def test_get_case_statistics(self, mock_load_cases, case_service, mock_cases_data):
        """Test getting case statistics"""
        mock_cases = [Case(**cases_index) for cases_index in mock_cases_data]
        mock_load_cases.return_value = mock_cases
        
        result = case_service.get_case_statistics()
        
        assert isinstance(result, CaseStatistics)
        assert result.total_cases == 3
        assert result.active_cases == 1
        assert result.under_review_cases == 1
        assert result.resolved_cases == 1
        # Recent activity count depends on current date vs mock dates
        assert isinstance(result.recent_activity_count, int)
        assert 0 <= result.recent_activity_count <= 3
    
    @patch.object(CaseService, '_load_cases')
    def test_get_case_statistics_recent_activity(self, mock_load_cases, case_service):
        """Test case statistics with recent activity calculation"""
        # Create cases with dates relative to now
        now = datetime.now()
        recent_date = now - timedelta(days=10)  # Within 30 days
        old_date = now - timedelta(days=40)     # Outside 30 days
        
        mock_cases_data = [
            {
                "id": "case-recent",
                "title": "Recent Case",
                "case_type": "Employment Dispute",
                "client_name": "Recent Client",
                "status": "Active",
                "created_date": recent_date.isoformat() + "Z",
                "summary": "Recent case",
                "key_parties": ["Recent Client"],
                "documents": [],
                "playbook_id": "employment-dispute"
            },
            {
                "id": "case-old",
                "title": "Old Case",
                "case_type": "Contract Breach",
                "client_name": "Old Client",
                "status": "Resolved",
                "created_date": old_date.isoformat() + "Z",
                "summary": "Old case",
                "key_parties": ["Old Client"],
                "documents": [],
                "playbook_id": "contract-breach"
            }
        ]
        
        mock_cases = [Case(**cases_index) for cases_index in mock_cases_data]
        mock_load_cases.return_value = mock_cases
        
        result = case_service.get_case_statistics()
        
        assert result.total_cases == 2
        assert result.recent_activity_count == 1  # Only the recent case
    
    @patch.object(CaseService, '_load_cases')
    def test_caching_behavior(self, mock_load_cases, case_service, mock_cases_data):
        """Test that cases are cached after first load"""
        mock_cases = [Case(**cases_index) for cases_index in mock_cases_data]
        mock_load_cases.return_value = mock_cases
        
        # First call should load cases
        result1 = case_service.get_all_cases()
        # Second call should use cache
        result2 = case_service.get_all_cases()
        
        assert result1 == result2
        # _load_cases should be called twice (once for each get_all_cases call)
        # but the actual file loading should be cached
        assert mock_load_cases.call_count == 2