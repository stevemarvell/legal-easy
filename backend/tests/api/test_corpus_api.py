#!/usr/bin/env python3
"""Corpus API Integration Tests"""

import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


class TestCorpusAPI:
    """Test Corpus API endpoints with real data"""
    
    def test_get_corpus_items(self):
        """Test GET /api/corpus/"""
        response = client.get("/api/corpus/")
        assert response.status_code == 200
        
        items = response.json()
        assert isinstance(items, list)
        
        # Verify item structure if items exist
        for item in items:
            assert 'id' in item
            assert 'name' in item
            assert 'category' in item
    
    def test_get_corpus_categories(self):
        """Test GET /api/corpus/categories"""
        response = client.get("/api/corpus/categories")
        assert response.status_code == 200
        
        categories = response.json()
        assert isinstance(categories, dict)
    
    def test_search_corpus(self):
        """Test GET /api/corpus/search"""
        response = client.get("/api/corpus/search?q=employment")
        assert response.status_code == 200
        
        results = response.json()
        assert 'items' in results
        assert 'total_count' in results
        assert 'query' in results
        assert results['query'] == 'employment'
        assert isinstance(results['items'], list)
        assert isinstance(results['total_count'], int)
    
    def test_get_corpus_concepts(self):
        """Test GET /api/corpus/concepts"""
        response = client.get("/api/corpus/concepts")
        assert response.status_code == 200
        
        concepts = response.json()
        assert 'concepts' in concepts
        assert 'total_concepts' in concepts
        assert isinstance(concepts['concepts'], list)
    
    def test_get_corpus_item_not_found(self):
        """Test GET /api/corpus/{item_id} with non-existent ID"""
        response = client.get("/api/corpus/nonexistent-item-id")
        assert response.status_code == 404
        
        error = response.json()
        assert 'detail' in error