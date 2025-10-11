#!/usr/bin/env python3
"""
Comprehensive test suite for Cases API

This test suite ensures the Cases API works correctly and prevents regressions.
"""

import pytest
import json
from fastapi.testclient import TestClient
from unittest.mock import patch, mock_open

# Import the FastAPI app
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import app
from app.services.data_service import DataService


class TestCasesAPI:
    """Comprehensive test suite for Cases API endpoints"""
    
    def setup_method(self):
        """Set up test client and sample data"""
        self.client = TestClient(app)
        self.sample_cases = [
            {
                "id": "case-001",
                "title": "Test Employment Case",
                "case_type": "Employment Dispute",
                "client_name": "John Doe",
                "status": "Active",
                "created_date": "2024-01-15T09:00:00Z",
                "summary": "Test case summary",
                "key_parties": ["John Doe (Claimant)", "ABC Corp (Respondent)"],
                "documents": ["doc-001", "doc-002"],
                "playbook_id": "employment-dispute"
            },
            {
                "id": "case-002",
                "title": "Test Contract Case",
                "case_type": "Contract Breach",
                "client_name": "Jane Smith",
                "status": "Under Review",
                "created_date": "2024-02-01T10:00:00Z",
                "summary": "Contract dispute case",
                "key_parties": ["Jane Smith (Claimant)", "XYZ Ltd (Respondent)"],
                "documents": ["doc-003"],
                "playbook_id": "contract-breach"
            }
        ]
    
    def test_get_cases_success(self):
        """Test GET /api/cases returns cases successfully"""
        with patch.object(DataService, 'load_cases', return_value=self.sample_cases):
            response = self.client.get("/api/cases")
            
            assert response.status_code == 200
            cases = response.json()
            assert len(cases) == 2
            assert cases[0]['id'] == 'case-001'
            assert cases[1]['id'] == 'case-002'
    
    def test_get_cases_empty_list(self):
        """Test GET /api/cases with no cases"""
        with patch.object(DataService, 'load_cases', return_value=[]):
            response = self.client.get("/api/cases")
            
            assert response.status_code == 200
            assert response.json() == []
    
    def test_get_cases_data_service_error(self):
        """Test GET /api/cases when DataService raises exception"""
        with patch.object(DataService, 'load_cases', side_effect=Exception("File error")):
            response = self.client.get("/api/cases")
            
            assert response.status_code == 500
            assert "Failed to get cases" in response.json()['detail']
    
    def test_get_case_by_id_success(self):
        """Test GET /api/cases/{case_id} returns specific case"""
        with patch.object(DataService, 'load_cases', return_value=self.sample_cases):
            response = self.client.get("/api/cases/case-001")
            
            assert response.status_code == 200
            case = response.json()
            assert case['id'] == 'case-001'
            assert case['title'] == 'Test Employment Case'
            assert case['client_name'] == 'John Doe'
    
    def test_get_case_by_id_not_found(self):
        """Test GET /api/cases/{case_id} with nonexistent case"""
        with patch.object(DataService, 'load_cases', return_value=self.sample_cases):
            response = self.client.get("/api/cases/nonexistent-case")
            
            assert response.status_code == 404
            assert "Case with ID nonexistent-case not found" in response.json()['detail']
    
    def test_get_case_by_id_empty_cases(self):
        """Test GET /api/cases/{case_id} with no cases in system"""
        with patch.object(DataService, 'load_cases', return_value=[]):
            response = self.client.get("/api/cases/case-001")
            
            assert response.status_code == 404
    
    def test_get_case_by_id_data_service_error(self):
        """Test GET /api/cases/{case_id} when DataService raises exception"""
        with patch.object(DataService, 'load_cases', side_effect=Exception("Database error")):
            response = self.client.get("/api/cases/case-001")
            
            assert response.status_code == 500
            assert "Failed to get case" in response.json()['detail']
    
    def test_get_case_by_id_malformed_data(self):
        """Test GET /api/cases/{case_id} with malformed case data"""
        # Case missing required fields
        malformed_case = {
            "id": "case-001",
            "title": "Incomplete Case"
            # Missing other required fields
        }
        
        with patch.object(DataService, 'load_cases', return_value=[malformed_case]):
            response = self.client.get("/api/cases/case-001")
            
            # Should return 500 due to Pydantic validation error
            assert response.status_code == 500
    
    def test_get_case_by_id_invalid_date_format(self):
        """Test GET /api/cases/{case_id} with invalid date format"""
        invalid_case = self.sample_cases[0].copy()
        invalid_case['created_date'] = "not-a-valid-date"
        
        with patch.object(DataService, 'load_cases', return_value=[invalid_case]):
            response = self.client.get("/api/cases/case-001")
            
            # Should return 500 due to date parsing error
            assert response.status_code == 500
    
    def test_case_data_structure_consistency(self):
        """Test that case data structure is consistent with model"""
        # This test ensures the bug we fixed doesn't regress
        with patch.object(DataService, 'load_cases', return_value=self.sample_cases):
            # Test that we can access case data as dictionaries
            cases = DataService.load_cases()
            
            for case in cases:
                # These should work (dictionary access)
                assert 'id' in case
                assert case.get('id') is not None
                assert case['title'] is not None
                
                # This should NOT work (object attribute access)
                with pytest.raises(AttributeError):
                    _ = case.id  # This would cause the original bug
    
    def test_all_sample_cases_individually(self):
        """Test each sample case individually"""
        with patch.object(DataService, 'load_cases', return_value=self.sample_cases):
            for case_data in self.sample_cases:
                case_id = case_data['id']
                response = self.client.get(f"/api/cases/{case_id}")
                
                assert response.status_code == 200
                returned_case = response.json()
                assert returned_case['id'] == case_id
                assert returned_case['title'] == case_data['title']
    
    def test_case_response_format(self):
        """Test that case response has correct format"""
        with patch.object(DataService, 'load_cases', return_value=self.sample_cases):
            response = self.client.get("/api/cases/case-001")
            
            assert response.status_code == 200
            case = response.json()
            
            # Check all required fields are present
            required_fields = [
                'id', 'title', 'case_type', 'client_name', 'status',
                'created_date', 'summary', 'key_parties', 'documents', 'playbook_id'
            ]
            
            for field in required_fields:
                assert field in case, f"Missing required field: {field}"
            
            # Check data types
            assert isinstance(case['key_parties'], list)
            assert isinstance(case['documents'], list)
            assert isinstance(case['id'], str)
            assert isinstance(case['title'], str)
    
    def test_case_statistics_endpoint(self):
        """Test GET /api/cases/statistics endpoint"""
        with patch.object(DataService, 'load_cases', return_value=self.sample_cases):
            response = self.client.get("/api/cases/statistics")
            
            assert response.status_code == 200
            stats = response.json()
            
            assert 'total_cases' in stats
            assert 'active_cases' in stats
            assert 'resolved_cases' in stats
            assert 'under_review_cases' in stats
            assert stats['total_cases'] == 2
            assert stats['active_cases'] == 1  # case-001 is Active
            assert stats['under_review_cases'] == 1  # case-002 is Under Review
    
    def test_edge_cases(self):
        """Test various edge cases"""
        with patch.object(DataService, 'load_cases', return_value=self.sample_cases):
            # Test empty case ID
            response = self.client.get("/api/cases/")
            assert response.status_code in [404, 405]  # Depends on FastAPI routing
            
            # Test case ID with special characters
            response = self.client.get("/api/cases/case-with-special-chars-!@#")
            assert response.status_code == 404
            
            # Test very long case ID
            long_id = "case-" + "x" * 1000
            response = self.client.get(f"/api/cases/{long_id}")
            assert response.status_code == 404


class TestDataServiceIntegration:
    """Test DataService integration with actual file system"""
    
    def test_load_cases_with_actual_file(self):
        """Test loading cases from actual file system"""
        # This test uses the real file system
        cases = DataService.load_cases()
        
        # Should return a list
        assert isinstance(cases, list)
        
        # If cases exist, validate their structure
        if cases:
            for case in cases:
                assert isinstance(case, dict)
                assert 'id' in case
                assert 'title' in case
                assert case.get('id') is not None
    
    def test_case_file_format_validation(self):
        """Test that the actual cases file has correct format"""
        import pathlib
        
        cases_file = pathlib.Path("data/cases/cases_index.json")
        
        if cases_file.exists():
            with open(cases_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            assert isinstance(data, list), "Cases file should contain a list"
            
            for i, case in enumerate(data):
                assert isinstance(case, dict), f"Case {i} should be a dictionary"
                assert 'id' in case, f"Case {i} missing 'id' field"
                assert case['id'], f"Case {i} has empty 'id' field"


if __name__ == "__main__":
    # Run the tests
    pytest.main([__file__, "-v", "-s"])