#!/usr/bin/env python3
"""
Comprehensive test suite for diagnosing Cases API 500 errors

This test suite will help identify the root cause of 500 errors when getting cases.
"""

import pytest
import json
import os
from pathlib import Path
from datetime import datetime
from fastapi.testclient import TestClient
from unittest.mock import patch, mock_open

# Import the FastAPI app and dependencies
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import app
from app.services.data_service import DataService
from app.models.case import Case


class TestCasesAPIDebug:
    """Test suite to diagnose Cases API issues"""
    
    def setup_method(self):
        """Set up test client"""
        self.client = TestClient(app)
        self.valid_case_data = {
            "id": "case-001",
            "title": "Test Case",
            "case_type": "Employment Dispute",
            "client_name": "Test Client",
            "status": "Active",
            "created_date": "2024-01-15T09:00:00Z",
            "summary": "Test summary",
            "key_parties": ["Party 1", "Party 2"],
            "documents": ["doc-001"],
            "playbook_id": "employment-dispute"
        }
    
    def test_data_service_load_cases_file_exists(self):
        """Test DataService.load_cases when file exists"""
        test_cases = [self.valid_case_data]
        
        with patch('pathlib.Path.exists', return_value=True):
            with patch('builtins.open', mock_open(read_data=json.dumps(test_cases))):
                cases = DataService.load_cases()
                assert len(cases) == 1
                assert cases[0]['id'] == 'case-001'
    
    def test_data_service_load_cases_file_not_exists(self):
        """Test DataService.load_cases when file doesn't exist"""
        with patch('pathlib.Path.exists', return_value=False):
            cases = DataService.load_cases()
            assert cases == []
    
    def test_data_service_load_cases_invalid_json(self):
        """Test DataService.load_cases with invalid JSON"""
        with patch('pathlib.Path.exists', return_value=True):
            with patch('builtins.open', mock_open(read_data='invalid json')):
                cases = DataService.load_cases()
                assert cases == []  # Should return empty list on error
    
    def test_data_service_load_cases_permission_error(self):
        """Test DataService.load_cases with file permission error"""
        with patch('pathlib.Path.exists', return_value=True):
            with patch('builtins.open', side_effect=PermissionError("Permission denied")):
                cases = DataService.load_cases()
                assert cases == []  # Should return empty list on error
    
    def test_case_model_validation_valid_data(self):
        """Test Case model with valid data"""
        try:
            case = Case(**self.valid_case_data)
            assert case.id == "case-001"
            assert case.title == "Test Case"
            assert isinstance(case.created_date, datetime)
        except Exception as e:
            pytest.fail(f"Valid case data should not raise exception: {e}")
    
    def test_case_model_validation_invalid_date(self):
        """Test Case model with invalid date format"""
        invalid_data = self.valid_case_data.copy()
        invalid_data['created_date'] = "invalid-date"
        
        with pytest.raises(Exception):
            Case(**invalid_data)
    
    def test_case_model_validation_missing_required_field(self):
        """Test Case model with missing required field"""
        invalid_data = self.valid_case_data.copy()
        del invalid_data['title']
        
        with pytest.raises(Exception):
            Case(**invalid_data)
    
    def test_case_model_validation_invalid_enum(self):
        """Test Case model with invalid enum value"""
        invalid_data = self.valid_case_data.copy()
        invalid_data['status'] = "Invalid Status"
        
        # Note: The current model doesn't enforce enum validation strictly
        # This test documents the current behavior
        try:
            case = Case(**invalid_data)
            # If this passes, the enum validation is not strict
            assert case.status == "Invalid Status"
        except Exception:
            # If this fails, enum validation is working
            pass
    
    def test_get_cases_endpoint_success(self):
        """Test GET /api/cases endpoint success"""
        test_cases = [self.valid_case_data]
        
        with patch.object(DataService, 'load_cases', return_value=test_cases):
            response = self.client.get("/api/cases")
            assert response.status_code == 200
            data = response.json()
            assert len(data) == 1
            assert data[0]['id'] == 'case-001'
    
    def test_get_cases_endpoint_empty_list(self):
        """Test GET /api/cases endpoint with empty list"""
        with patch.object(DataService, 'load_cases', return_value=[]):
            response = self.client.get("/api/cases")
            assert response.status_code == 200
            assert response.json() == []
    
    def test_get_cases_endpoint_data_service_exception(self):
        """Test GET /api/cases endpoint when DataService raises exception"""
        with patch.object(DataService, 'load_cases', side_effect=Exception("Database error")):
            response = self.client.get("/api/cases")
            assert response.status_code == 500
            assert "Failed to get cases" in response.json()['detail']
    
    def test_get_case_by_id_success(self):
        """Test GET /api/cases/{case_id} endpoint success"""
        test_cases = [self.valid_case_data]
        
        with patch.object(DataService, 'load_cases', return_value=test_cases):
            response = self.client.get("/api/cases/case-001")
            assert response.status_code == 200
            data = response.json()
            assert data['id'] == 'case-001'
            assert data['title'] == 'Test Case'
    
    def test_get_case_by_id_not_found(self):
        """Test GET /api/cases/{case_id} endpoint case not found"""
        test_cases = [self.valid_case_data]
        
        with patch.object(DataService, 'load_cases', return_value=test_cases):
            response = self.client.get("/api/cases/nonexistent-case")
            assert response.status_code == 404
            assert "Case with ID nonexistent-case not found" in response.json()['detail']
    
    def test_get_case_by_id_empty_cases_list(self):
        """Test GET /api/cases/{case_id} endpoint with empty cases list"""
        with patch.object(DataService, 'load_cases', return_value=[]):
            response = self.client.get("/api/cases/case-001")
            assert response.status_code == 404
    
    def test_get_case_by_id_data_service_exception(self):
        """Test GET /api/cases/{case_id} endpoint when DataService raises exception"""
        with patch.object(DataService, 'load_cases', side_effect=Exception("File not found")):
            response = self.client.get("/api/cases/case-001")
            assert response.status_code == 500
            assert "Failed to get case" in response.json()['detail']
    
    def test_get_case_by_id_invalid_case_data(self):
        """Test GET /api/cases/{case_id} endpoint with invalid case data from file"""
        # Case data missing required fields
        invalid_case = {
            "id": "case-001",
            "title": "Test Case"
            # Missing required fields
        }
        
        with patch.object(DataService, 'load_cases', return_value=[invalid_case]):
            response = self.client.get("/api/cases/case-001")
            # This might cause a 500 error due to Pydantic validation
            # The exact behavior depends on how FastAPI handles the response
            assert response.status_code in [200, 500]  # Document current behavior
    
    def test_get_case_by_id_malformed_date(self):
        """Test GET /api/cases/{case_id} endpoint with malformed date"""
        invalid_case = self.valid_case_data.copy()
        invalid_case['created_date'] = "not-a-date"
        
        with patch.object(DataService, 'load_cases', return_value=[invalid_case]):
            response = self.client.get("/api/cases/case-001")
            # This should cause a 500 error due to date parsing
            assert response.status_code == 500
    
    def test_actual_file_system_cases_load(self):
        """Test loading cases from actual file system"""
        try:
            cases = DataService.load_cases()
            print(f"Loaded {len(cases)} cases from file system")
            
            if cases:
                # Test that we can create Case models from the loaded data
                for i, case_data in enumerate(cases):
                    try:
                        case = Case(**case_data)
                        print(f"Case {i+1}: {case.id} - {case.title} ✓")
                    except Exception as e:
                        print(f"Case {i+1}: Failed to validate - {e}")
                        pytest.fail(f"Case data validation failed for case {i+1}: {e}")
            
        except Exception as e:
            pytest.fail(f"Failed to load cases from file system: {e}")
    
    def test_actual_api_endpoints_integration(self):
        """Integration test with actual file system"""
        # Test the actual endpoints without mocking
        try:
            # Test cases list
            response = self.client.get("/api/cases")
            print(f"GET /api/cases - Status: {response.status_code}")
            
            if response.status_code != 200:
                print(f"Error response: {response.text}")
                pytest.fail(f"Cases list endpoint failed: {response.status_code}")
            
            cases = response.json()
            print(f"Retrieved {len(cases)} cases")
            
            if cases:
                # Test individual case endpoint
                first_case_id = cases[0]['id']
                response = self.client.get(f"/api/cases/{first_case_id}")
                print(f"GET /api/cases/{first_case_id} - Status: {response.status_code}")
                
                if response.status_code != 200:
                    print(f"Error response: {response.text}")
                    pytest.fail(f"Individual case endpoint failed: {response.status_code}")
                
                case_data = response.json()
                print(f"Retrieved case: {case_data.get('title', 'Unknown')}")
        
        except Exception as e:
            pytest.fail(f"Integration test failed: {e}")


class TestCasesDataValidation:
    """Test suite specifically for data validation issues"""
    
    def test_cases_index_file_structure(self):
        """Test the structure of the actual cases index file"""
        cases_file = Path("data/cases/cases_index.json")
        
        if not cases_file.exists():
            pytest.skip("Cases index file not found")
        
        try:
            with open(cases_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            assert isinstance(data, list), "Cases data should be a list"
            
            for i, case in enumerate(data):
                assert isinstance(case, dict), f"Case {i} should be a dictionary"
                
                # Check required fields
                required_fields = ['id', 'title', 'case_type', 'client_name', 'status', 
                                 'created_date', 'summary', 'key_parties', 'documents', 'playbook_id']
                
                for field in required_fields:
                    assert field in case, f"Case {i} missing required field: {field}"
                
                # Validate date format
                try:
                    datetime.fromisoformat(case['created_date'].replace('Z', '+00:00'))
                except ValueError as e:
                    pytest.fail(f"Case {i} has invalid date format: {case['created_date']} - {e}")
                
                # Validate data types
                assert isinstance(case['key_parties'], list), f"Case {i} key_parties should be a list"
                assert isinstance(case['documents'], list), f"Case {i} documents should be a list"
        
        except Exception as e:
            pytest.fail(f"Failed to validate cases index file: {e}")


if __name__ == "__main__":
    # Run the tests
    pytest.main([__file__, "-v", "-s"])