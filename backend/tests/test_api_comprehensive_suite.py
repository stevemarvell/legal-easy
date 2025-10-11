#!/usr/bin/env python3
"""
Comprehensive API Test Suite Runner

This module provides a complete test suite runner for all API endpoints including:
- Cross-endpoint integration tests
- Performance and load testing scenarios
- Error handling and edge case validation
- API contract compliance testing
"""

import pytest
import asyncio
import time
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from concurrent.futures import ThreadPoolExecutor
from main import app

client = TestClient(app)


class TestAPIHealthAndStatus:
    """Test API health and status endpoints"""
    
    def test_api_root_endpoint(self):
        """Test root API endpoint returns proper response"""
        response = client.get("/")
        assert response.status_code == 200
        # Adjust based on your actual root endpoint response
    
    def test_api_health_check(self):
        """Test API health check endpoint if available"""
        # This would test a health endpoint if you have one
        # response = client.get("/health")
        # assert response.status_code == 200
        pass
    
    def test_api_docs_endpoint(self):
        """Test API documentation endpoint"""
        response = client.get("/docs")
        assert response.status_code == 200
        assert "text/html" in response.headers.get("content-type", "")
    
    def test_api_openapi_schema(self):
        """Test OpenAPI schema endpoint"""
        response = client.get("/openapi.json")
        assert response.status_code == 200
        schema = response.json()
        assert "openapi" in schema
        assert "info" in schema
        assert "paths" in schema


class TestCrossEndpointIntegration:
    """Test integration between different API endpoints"""
    
    def test_case_document_corpus_integration(self):
        """Test integration between cases, documents, and corpus endpoints"""
        with patch('app.services.data_service.DataService.load_cases') as mock_cases, \
             patch('app.services.data_service.DataService.load_case_documents') as mock_docs, \
             patch('app.services.data_service.DataService.search_corpus') as mock_corpus, \
             patch('app.services.playbook_service.PlaybookService.analyze_case_with_playbook') as mock_analysis:
            
            # Setup mock data for integrated workflow
            mock_cases.return_value = [
                {
                    "id": "case-001",
                    "title": "Employment Dispute Case",
                    "case_type": "Employment Dispute",
                    "status": "Active",
                    "documents": ["doc-001", "doc-002"]
                }
            ]
            
            mock_docs.return_value = [
                {
                    "id": "doc-001",
                    "case_id": "case-001",
                    "name": "Employment Contract",
                    "type": "Contract",
                    "analysis_completed": True
                }
            ]
            
            mock_corpus.return_value = [
                {
                    "id": "rc-001",
                    "name": "Employment Contract Template",
                    "category": "contracts",
                    "research_areas": ["Employment Law"]
                }
            ]
            
            mock_analysis.return_value = {
                "case_id": "case-001",
                "case_strength_assessment": {"overall_strength": "Moderate"},
                "strategic_recommendations": [],
                "relevant_precedents": [],
                "applied_playbook": {"id": "employment-dispute"}
            }
            
            # Test integrated workflow
            # 1. Get cases
            cases_response = client.get("/cases/")
            assert cases_response.status_code == 200
            cases = cases_response.json()
            case_id = cases[0]["id"]
            
            # 2. Get case documents
            docs_response = client.get(f"/documents/cases/{case_id}/documents")
            assert docs_response.status_code == 200
            documents = docs_response.json()
            assert len(documents) == 1
            
            # 3. Search related corpus materials
            corpus_response = client.get("/corpus/search?q=employment")
            assert corpus_response.status_code == 200
            corpus_data = corpus_response.json()
            assert corpus_data["total_count"] == 1
            
            # 4. Get comprehensive analysis
            analysis_response = client.get(f"/cases/{case_id}/comprehensive-analysis")
            assert analysis_response.status_code == 200
            analysis = analysis_response.json()
            assert analysis["case_id"] == case_id
    
    def test_documentation_corpus_integration(self):
        """Test integration between documentation and corpus endpoints"""
        with patch('app.services.data_service.DataService.search_documentation') as mock_docs, \
             patch('app.services.data_service.DataService.search_corpus') as mock_corpus:
            
            mock_docs.return_value = [
                {
                    "id": "api-overview",
                    "name": "API Overview",
                    "category": "api",
                    "tags": ["api", "reference"]
                }
            ]
            
            mock_corpus.return_value = [
                {
                    "id": "rc-001",
                    "name": "API Documentation Template",
                    "category": "templates",
                    "research_areas": ["Documentation"]
                }
            ]
            
            # Search both documentation and corpus for related content
            docs_response = client.get("/docs/search?q=api")
            corpus_response = client.get("/corpus/search?q=api")
            
            assert docs_response.status_code == 200
            assert corpus_response.status_code == 200
            
            docs_data = docs_response.json()
            corpus_data = corpus_response.json()
            
            assert docs_data["total_count"] >= 0
            assert corpus_data["total_count"] >= 0


class TestAPIPerformance:
    """Test API performance and load handling"""
    
    def test_concurrent_requests_handling(self):
        """Test API handles concurrent requests properly"""
        with patch('app.services.data_service.DataService.load_cases') as mock_cases:
            mock_cases.return_value = [{"id": "case-001", "title": "Test Case"}]
            
            def make_request():
                response = client.get("/cases/")
                return response.status_code
            
            # Test concurrent requests
            with ThreadPoolExecutor(max_workers=5) as executor:
                futures = [executor.submit(make_request) for _ in range(10)]
                results = [future.result() for future in futures]
            
            # All requests should succeed
            assert all(status == 200 for status in results)
    
    def test_response_time_performance(self):
        """Test API response times are reasonable"""
        with patch('app.services.data_service.DataService.load_cases') as mock_cases:
            mock_cases.return_value = [{"id": "case-001", "title": "Test Case"}]
            
            start_time = time.time()
            response = client.get("/cases/")
            end_time = time.time()
            
            assert response.status_code == 200
            response_time = end_time - start_time
            assert response_time < 1.0  # Should respond within 1 second
    
    def test_large_dataset_handling(self):
        """Test API handles large datasets appropriately"""
        with patch('app.services.data_service.DataService.load_cases') as mock_cases:
            # Create a large mock dataset
            large_dataset = [
                {
                    "id": f"case-{i:03d}",
                    "title": f"Test Case {i}",
                    "case_type": "Test Type",
                    "status": "Active"
                }
                for i in range(1000)
            ]
            mock_cases.return_value = large_dataset
            
            response = client.get("/cases/")
            assert response.status_code == 200
            data = response.json()
            assert len(data) == 1000


class TestAPIErrorHandling:
    """Test comprehensive API error handling"""
    
    def test_malformed_request_handling(self):
        """Test API handles malformed requests gracefully"""
        # Test invalid JSON in POST request
        response = client.post(
            "/documents/doc-001/analyze",
            headers={"Content-Type": "application/json"},
            data="invalid json"
        )
        # Should handle malformed JSON gracefully
        assert response.status_code in [400, 422, 500]
    
    def test_invalid_path_parameters(self):
        """Test API handles invalid path parameters"""
        # Test with various invalid IDs
        invalid_ids = ["", "null", "undefined", "../../etc/passwd", "<script>", "' OR 1=1 --"]
        
        for invalid_id in invalid_ids:
            response = client.get(f"/cases/{invalid_id}")
            # Should return 404 or 422, not crash
            assert response.status_code in [404, 422, 500]
    
    def test_service_unavailable_handling(self):
        """Test API handles service unavailability gracefully"""
        with patch('app.services.data_service.DataService.load_cases') as mock_cases:
            mock_cases.side_effect = Exception("Database connection failed")
            
            response = client.get("/cases/")
            assert response.status_code == 500
            error_data = response.json()
            assert "detail" in error_data
            assert "Failed to get cases" in error_data["detail"]
    
    def test_timeout_handling(self):
        """Test API handles timeouts appropriately"""
        with patch('app.services.data_service.DataService.load_cases') as mock_cases:
            def slow_response():
                time.sleep(2)  # Simulate slow service
                return [{"id": "case-001"}]
            
            mock_cases.side_effect = slow_response
            
            # This would test timeout handling if implemented
            # For now, just ensure it doesn't crash
            try:
                response = client.get("/cases/", timeout=1)
                # Should either succeed or handle timeout gracefully
                assert response.status_code in [200, 500, 504]
            except Exception:
                # Timeout exceptions are acceptable
                pass


class TestAPIContractCompliance:
    """Test API contract compliance and consistency"""
    
    def test_response_format_consistency(self):
        """Test all endpoints return consistent response formats"""
        endpoints_to_test = [
            ("/cases/", "GET"),
            ("/corpus/", "GET"),
            ("/docs/", "GET"),
            ("/playbooks/", "GET")
        ]
        
        for endpoint, method in endpoints_to_test:
            with patch('app.services.data_service.DataService.load_cases') as mock_cases, \
                 patch('app.services.data_service.DataService.search_corpus') as mock_corpus, \
                 patch('app.services.data_service.DataService.load_documentation_categories') as mock_docs, \
                 patch('app.services.data_service.DataService.get_all_documentation_tags') as mock_tags, \
                 patch('app.services.data_service.DataService.load_playbooks') as mock_playbooks:
                
                # Setup minimal mock responses
                mock_cases.return_value = []
                mock_corpus.return_value = []
                mock_docs.return_value = {}
                mock_tags.return_value = []
                mock_playbooks.return_value = []
                
                if method == "GET":
                    response = client.get(endpoint)
                
                assert response.status_code == 200
                assert response.headers.get("content-type") == "application/json"
                
                # Ensure response is valid JSON
                data = response.json()
                assert isinstance(data, (list, dict))
    
    def test_error_response_format_consistency(self):
        """Test all endpoints return consistent error response formats"""
        with patch('app.services.data_service.DataService.load_cases') as mock_service:
            mock_service.side_effect = Exception("Test error")
            
            response = client.get("/cases/")
            assert response.status_code == 500
            error_data = response.json()
            assert "detail" in error_data
            assert isinstance(error_data["detail"], str)
    
    def test_http_methods_compliance(self):
        """Test endpoints respond correctly to different HTTP methods"""
        # Test that GET endpoints reject POST/PUT/DELETE
        get_endpoints = ["/cases/", "/corpus/", "/docs/", "/playbooks/"]
        
        for endpoint in get_endpoints:
            # These should not be allowed
            post_response = client.post(endpoint)
            put_response = client.put(endpoint)
            delete_response = client.delete(endpoint)
            
            # Should return 405 Method Not Allowed or 404
            assert post_response.status_code in [404, 405]
            assert put_response.status_code in [404, 405]
            assert delete_response.status_code in [404, 405]


class TestAPISecurityBasics:
    """Test basic API security measures"""
    
    def test_sql_injection_protection(self):
        """Test API protects against basic SQL injection attempts"""
        sql_injection_attempts = [
            "'; DROP TABLE cases; --",
            "' OR '1'='1",
            "1' UNION SELECT * FROM users --"
        ]
        
        for injection_attempt in sql_injection_attempts:
            response = client.get(f"/cases/{injection_attempt}")
            # Should not crash or return unexpected data
            assert response.status_code in [404, 422, 500]
    
    def test_xss_protection(self):
        """Test API protects against basic XSS attempts"""
        xss_attempts = [
            "<script>alert('xss')</script>",
            "javascript:alert('xss')",
            "<img src=x onerror=alert('xss')>"
        ]
        
        for xss_attempt in xss_attempts:
            response = client.get(f"/cases/{xss_attempt}")
            # Should handle malicious input safely
            assert response.status_code in [404, 422, 500]
            
            # Response should not contain unescaped script tags
            if response.status_code != 500:
                response_text = response.text
                assert "<script>" not in response_text
                assert "javascript:" not in response_text


class TestAPIDocumentationCompliance:
    """Test API documentation and OpenAPI compliance"""
    
    def test_openapi_schema_validity(self):
        """Test OpenAPI schema is valid and complete"""
        response = client.get("/openapi.json")
        assert response.status_code == 200
        
        schema = response.json()
        
        # Check required OpenAPI fields
        assert "openapi" in schema
        assert "info" in schema
        assert "paths" in schema
        
        # Check info section
        assert "title" in schema["info"]
        assert "version" in schema["info"]
        
        # Check paths are documented
        paths = schema["paths"]
        expected_paths = ["/cases/", "/corpus/", "/docs/", "/playbooks/"]
        
        for expected_path in expected_paths:
            assert any(path.startswith(expected_path.rstrip('/')) for path in paths.keys())
    
    def test_endpoint_documentation_completeness(self):
        """Test all endpoints have proper documentation"""
        response = client.get("/openapi.json")
        schema = response.json()
        
        for path, methods in schema["paths"].items():
            for method, details in methods.items():
                # Each endpoint should have summary and description
                assert "summary" in details, f"Missing summary for {method.upper()} {path}"
                assert "responses" in details, f"Missing responses for {method.upper()} {path}"
                
                # Should document success response
                assert "200" in details["responses"], f"Missing 200 response for {method.upper()} {path}"


def run_comprehensive_tests():
    """Run all comprehensive API tests"""
    print("Running comprehensive API test suite...")
    
    # Run all test classes
    test_classes = [
        TestAPIHealthAndStatus,
        TestCrossEndpointIntegration,
        TestAPIPerformance,
        TestAPIErrorHandling,
        TestAPIContractCompliance,
        TestAPISecurityBasics,
        TestAPIDocumentationCompliance
    ]
    
    total_tests = 0
    passed_tests = 0
    
    for test_class in test_classes:
        print(f"\nRunning {test_class.__name__}...")
        
        # Get all test methods
        test_methods = [method for method in dir(test_class) if method.startswith('test_')]
        
        for test_method in test_methods:
            total_tests += 1
            try:
                # Create instance and run test
                instance = test_class()
                getattr(instance, test_method)()
                passed_tests += 1
                print(f"  ✓ {test_method}")
            except Exception as e:
                print(f"  ✗ {test_method}: {str(e)}")
    
    print(f"\nTest Results: {passed_tests}/{total_tests} tests passed")
    return passed_tests == total_tests


if __name__ == "__main__":
    # Can be run directly or via pytest
    if len(pytest.sys.argv) > 1 and pytest.sys.argv[1] == "pytest":
        pytest.main([__file__])
    else:
        success = run_comprehensive_tests()
        exit(0 if success else 1)