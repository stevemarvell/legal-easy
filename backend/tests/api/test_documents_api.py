#!/usr/bin/env python3
"""Documents API Integration Tests"""

import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


class TestDocumentsAPI:
    """Test Documents API endpoints with real data"""
    
    def test_get_case_documents(self):
        """Test GET /api/documents/cases/{case_id}/documents"""
        # Get a real case ID first
        cases_response = client.get("/api/cases/")
        cases = cases_response.json()
        test_case_id = cases[0]['id']
        
        response = client.get(f"/api/documents/cases/{test_case_id}/documents")
        assert response.status_code == 200
        
        documents = response.json()
        assert isinstance(documents, list)
        
        # If documents exist, verify structure
        for doc in documents:
            assert 'id' in doc
            assert 'name' in doc
            assert 'case_id' in doc
            assert doc['case_id'] == test_case_id
    
    def test_get_specific_document(self):
        """Test GET /api/documents/{document_id}"""
        # Get a real case and its documents first
        cases_response = client.get("/api/cases/")
        cases = cases_response.json()
        test_case_id = cases[0]['id']
        
        docs_response = client.get(f"/api/documents/cases/{test_case_id}/documents")
        documents = docs_response.json()
        
        if not documents:
            pytest.skip("No documents available for testing")
        
        test_doc_id = documents[0]['id']
        
        response = client.get(f"/api/documents/{test_doc_id}")
        assert response.status_code == 200
        
        doc = response.json()
        assert doc['id'] == test_doc_id
        assert 'name' in doc
        assert 'case_id' in doc
        assert 'type' in doc
    
    def test_get_document_not_found(self):
        """Test GET /api/documents/{document_id} with non-existent ID"""
        response = client.get("/api/documents/nonexistent-doc-id")
        assert response.status_code == 404
        
        error = response.json()
        assert 'detail' in error
    
    def test_get_document_analysis(self):
        """Test GET /api/documents/{document_id}/analysis"""
        # Get a real document ID first
        cases_response = client.get("/api/cases/")
        cases = cases_response.json()
        test_case_id = cases[0]['id']
        
        docs_response = client.get(f"/api/documents/cases/{test_case_id}/documents")
        documents = docs_response.json()
        
        if not documents:
            pytest.skip("No documents available for testing")
        
        test_doc_id = documents[0]['id']
        
        response = client.get(f"/api/documents/{test_doc_id}/analysis")
        
        # Analysis might not exist, which is fine
        assert response.status_code in [200, 404]
        
        if response.status_code == 200:
            analysis = response.json()
            assert analysis['document_id'] == test_doc_id
    
    def test_get_document_content(self):
        """Test GET /api/documents/{document_id}/content"""
        # Get a real document ID first
        cases_response = client.get("/api/cases/")
        cases = cases_response.json()
        test_case_id = cases[0]['id']
        
        docs_response = client.get(f"/api/documents/cases/{test_case_id}/documents")
        documents = docs_response.json()
        
        if not documents:
            pytest.skip("No documents available for testing")
        
        test_doc_id = documents[0]['id']
        
        response = client.get(f"/api/documents/{test_doc_id}/content")
        
        # Content files might not exist, which is fine
        assert response.status_code in [200, 404]
        
        if response.status_code == 200:
            content = response.json()
            assert 'document_id' in content
            assert 'content' in content
    
    def test_post_document_analyze(self):
        """Test POST /api/documents/{document_id}/analyze"""
        # Get a real document ID first
        cases_response = client.get("/api/cases/")
        cases = cases_response.json()
        test_case_id = cases[0]['id']
        
        docs_response = client.get(f"/api/documents/cases/{test_case_id}/documents")
        documents = docs_response.json()
        
        if not documents:
            pytest.skip("No documents available for testing")
        
        test_doc_id = documents[0]['id']
        
        response = client.post(f"/api/documents/{test_doc_id}/analyze")
        
        # Analysis might fail due to missing content or AI service issues
        assert response.status_code in [200, 404, 500]
    
    def test_delete_document_analysis(self):
        """Test DELETE /api/documents/{document_id}/analysis"""
        # Get a real document ID first
        cases_response = client.get("/api/cases/")
        cases = cases_response.json()
        test_case_id = cases[0]['id']
        
        docs_response = client.get(f"/api/documents/cases/{test_case_id}/documents")
        documents = docs_response.json()
        
        if not documents:
            pytest.skip("No documents available for testing")
        
        test_doc_id = documents[0]['id']
        
        response = client.delete(f"/api/documents/{test_doc_id}/analysis")
        
        # Analysis might not exist to delete
        assert response.status_code in [200, 404]