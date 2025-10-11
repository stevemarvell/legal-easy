#!/usr/bin/env python3
"""Documentation API Integration Tests"""

import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


class TestDocsAPI:
    """Test Documentation API endpoints with real data"""
    
    def test_get_docs_overview(self):
        """Test GET /api/docs/"""
        response = client.get("/api/docs/")
        assert response.status_code == 200
        
        overview = response.json()
        assert 'categories' in overview
        assert 'total_documents' in overview
        assert isinstance(overview['categories'], dict)
        assert isinstance(overview['total_documents'], int)
    
    def test_search_docs(self):
        """Test GET /api/docs/search"""
        response = client.get("/api/docs/search?q=api")
        assert response.status_code == 200
        
        results = response.json()
        assert 'items' in results
        assert 'total_count' in results
        assert 'query' in results
        assert results['query'] == 'api'
        assert isinstance(results['items'], list)
    
    def test_get_json_schemas(self):
        """Test GET /api/docs/schemas"""
        response = client.get("/api/docs/schemas")
        assert response.status_code == 200
        
        schemas = response.json()
        assert 'schemas' in schemas
        assert 'total_count' in schemas
        assert isinstance(schemas['schemas'], list)
    
    def test_get_docs_by_category_not_found(self):
        """Test GET /api/docs/{category} with non-existent category"""
        response = client.get("/api/docs/nonexistent-category")
        assert response.status_code == 404
        
        error = response.json()
        assert 'detail' in error