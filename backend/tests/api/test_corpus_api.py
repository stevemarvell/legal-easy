#!/usr/bin/env python3
"""Corpus API Integration Tests"""

import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


class TestCorpusAPI:
    """Test Corpus API endpoints with real data"""
    
    def test_get_corpus_items(self):
        """Test GET /api/corpus/ - Browse all corpus items"""
        response = client.get("/api/corpus/")
        assert response.status_code == 200
        
        items = response.json()
        assert isinstance(items, list)
        assert len(items) > 0  # Should have corpus items
        
        # Verify item structure if items exist
        for item in items:
            assert 'id' in item
            assert 'title' in item
            assert 'category' in item
            assert 'legal_concepts' in item
            assert 'related_items' in item
            assert 'metadata' in item
    
    def test_get_corpus_items_by_category(self):
        """Test GET /api/corpus/?category=contracts - Browse corpus by specific category"""
        # Test contracts category
        response = client.get("/api/corpus/?category=contracts")
        assert response.status_code == 200
        
        items = response.json()
        assert isinstance(items, list)
        
        # All items should be contracts
        for item in items:
            assert item['category'] == 'contracts'
        
        # Test clauses category
        response = client.get("/api/corpus/?category=clauses")
        assert response.status_code == 200
        
        items = response.json()
        for item in items:
            assert item['category'] == 'clauses'
        
        # Test precedents category
        response = client.get("/api/corpus/?category=precedents")
        assert response.status_code == 200
        
        items = response.json()
        for item in items:
            assert item['category'] == 'precedents'
        
        # Test statutes category
        response = client.get("/api/corpus/?category=statutes")
        assert response.status_code == 200
        
        items = response.json()
        for item in items:
            assert item['category'] == 'statutes'
    
    def test_get_corpus_categories(self):
        """Test GET /api/corpus/categories - Get category list"""
        response = client.get("/api/corpus/categories")
        assert response.status_code == 200
        
        categories = response.json()
        assert isinstance(categories, dict)
        
        # Should have the four main categories
        expected_categories = ['contracts', 'clauses', 'precedents', 'statutes']
        for category in expected_categories:
            assert category in categories
            assert 'name' in categories[category]
            assert 'description' in categories[category]
            assert 'document_ids' in categories[category]
    
    def test_get_corpus_item_by_id(self):
        """Test GET /api/corpus/{id} - Get specific corpus item content"""
        # Test with a known corpus item ID
        response = client.get("/api/corpus/rc-001")
        assert response.status_code == 200
        
        item = response.json()
        assert item['id'] == 'rc-001'
        assert 'title' in item
        assert 'category' in item
        assert 'content' in item
        assert item['content'] is not None  # Should have full content
        assert len(item['content']) > 0
        
        # Test with another known ID
        response = client.get("/api/corpus/rc-002")
        assert response.status_code == 200
        
        item = response.json()
        assert item['id'] == 'rc-002'
        assert 'content' in item
    
    def test_search_corpus_basic(self):
        """Test GET /api/corpus/search - Basic concept-based search"""
        response = client.get("/api/corpus/search?q=employment")
        assert response.status_code == 200
        
        results = response.json()
        assert 'items' in results
        assert 'total_count' in results
        assert 'query' in results
        assert 'categories_found' in results
        assert 'research_areas_found' in results
        
        assert results['query'] == 'employment'
        assert isinstance(results['items'], list)
        assert isinstance(results['total_count'], int)
        assert results['total_count'] >= 0
        
        # Should find employment-related items
        if results['total_count'] > 0:
            assert 'Employment Law' in results['research_areas_found']
    
    def test_search_corpus_with_category_filter(self):
        """Test corpus search with category filtering"""
        # Search for employment in contracts only
        response = client.get("/api/corpus/search?q=employment&category=contracts")
        assert response.status_code == 200
        
        results = response.json()
        assert results['query'] == 'employment'
        
        # All results should be contracts
        for item in results['items']:
            assert item['category'] == 'contracts'
    
    def test_search_corpus_with_research_area_filter(self):
        """Test corpus search with research area filtering"""
        # Search with research area filter
        response = client.get("/api/corpus/search?q=contract&research_area=Employment Law")
        assert response.status_code == 200
        
        results = response.json()
        assert results['query'] == 'contract'
        
        # All results should have Employment Law in research areas
        for item in results['items']:
            assert 'Employment Law' in item.get('research_areas', [])
    
    def test_search_corpus_concept_based(self):
        """Test concept-based search functionality"""
        # Search for legal concepts
        response = client.get("/api/corpus/search?q=liability")
        assert response.status_code == 200
        
        results = response.json()
        assert 'items' in results
        assert 'categories_found' in results
        assert 'research_areas_found' in results
        
        # Search for intellectual property
        response = client.get("/api/corpus/search?q=intellectual property")
        assert response.status_code == 200
        
        results = response.json()
        if results['total_count'] > 0:
            assert 'Intellectual Property' in results['research_areas_found']
    
    def test_get_corpus_concepts(self):
        """Test GET /api/corpus/concepts - Get legal concept relationships"""
        response = client.get("/api/corpus/concepts")
        assert response.status_code == 200
        
        concepts = response.json()
        assert 'concepts' in concepts
        assert 'total_concepts' in concepts
        assert 'categories_analyzed' in concepts
        assert 'research_areas' in concepts
        
        assert isinstance(concepts['concepts'], list)
        assert isinstance(concepts['total_concepts'], int)
        assert concepts['total_concepts'] > 0
        
        # Should analyze all four categories
        expected_categories = ['contracts', 'clauses', 'precedents', 'statutes']
        for category in expected_categories:
            assert category in concepts['categories_analyzed']
        
        # Verify concept structure
        for concept in concepts['concepts']:
            assert 'id' in concept
            assert 'name' in concept
            assert 'definition' in concept
            assert 'related_concepts' in concept
            assert 'corpus_references' in concept
    
    def test_get_related_materials(self):
        """Test GET /api/corpus/{id}/related - Get related materials"""
        # Test with a known corpus item
        response = client.get("/api/corpus/rc-001/related")
        assert response.status_code == 200
        
        related_items = response.json()
        assert isinstance(related_items, list)
        
        # Should have related items
        if len(related_items) > 0:
            for item in related_items:
                assert 'id' in item
                assert 'title' in item
                assert 'category' in item
                assert item['id'] != 'rc-001'  # Should not include the original item
        
        # Test with another item
        response = client.get("/api/corpus/rc-002/related")
        assert response.status_code == 200
        
        related_items = response.json()
        assert isinstance(related_items, list)
    
    def test_get_related_materials_concept_relationships(self):
        """Test related materials based on legal concepts and relationships"""
        # Get an item and its related materials
        response = client.get("/api/corpus/rc-001")
        assert response.status_code == 200
        original_item = response.json()
        
        response = client.get("/api/corpus/rc-001/related")
        assert response.status_code == 200
        related_items = response.json()
        
        if len(related_items) > 0:
            # Related items should share research areas, categories, or legal concepts
            original_research_areas = set(original_item.get('research_areas', []))
            original_category = original_item.get('category')
            original_concepts = set(original_item.get('legal_concepts', []))
            
            for related_item in related_items:
                related_research_areas = set(related_item.get('research_areas', []))
                related_category = related_item.get('category')
                related_concepts = set(related_item.get('legal_concepts', []))
                
                # Should have some relationship
                has_shared_areas = bool(original_research_areas.intersection(related_research_areas))
                has_same_category = original_category == related_category
                has_shared_concepts = bool(original_concepts.intersection(related_concepts))
                
                assert has_shared_areas or has_same_category or has_shared_concepts
    
    def test_get_corpus_item_not_found(self):
        """Test GET /api/corpus/{item_id} with non-existent ID"""
        response = client.get("/api/corpus/nonexistent-item-id")
        assert response.status_code == 404
        
        error = response.json()
        assert 'detail' in error
        assert 'not found' in error['detail'].lower()
    
    def test_get_related_materials_not_found(self):
        """Test GET /api/corpus/{item_id}/related with non-existent ID"""
        response = client.get("/api/corpus/nonexistent-item-id/related")
        assert response.status_code == 404
        
        error = response.json()
        assert 'detail' in error
        assert 'not found' in error['detail'].lower()
    
    def test_search_corpus_empty_query(self):
        """Test search with empty query returns all items"""
        response = client.get("/api/corpus/search?q=")
        assert response.status_code == 200  # Empty query is allowed and returns all items
        
        results = response.json()
        assert 'items' in results
        assert 'total_count' in results
        assert results['query'] == ''
        # Should return all corpus items
        assert results['total_count'] > 0
    
    def test_corpus_browsing_different_categories(self):
        """Test browsing corpus with different categories comprehensively"""
        categories = ['contracts', 'clauses', 'precedents', 'statutes']
        
        for category in categories:
            response = client.get(f"/api/corpus/?category={category}")
            assert response.status_code == 200
            
            items = response.json()
            assert isinstance(items, list)
            
            # All items should belong to the requested category
            for item in items:
                assert item['category'] == category
                assert 'legal_concepts' in item
                assert 'research_areas' in item
    
    def test_concept_based_search_integration(self):
        """Test integration of concept-based search with legal concepts"""
        # Test various legal concept searches
        concept_queries = [
            'employment',
            'contract',
            'liability',
            'intellectual property',
            'data protection'
        ]
        
        for query in concept_queries:
            response = client.get(f"/api/corpus/search?q={query}")
            assert response.status_code == 200
            
            results = response.json()
            assert 'items' in results
            assert 'categories_found' in results
            assert 'research_areas_found' in results
            assert results['query'] == query
    
    def test_regenerate_corpus_index_success(self):
        """Test POST /api/corpus/regenerate-index - Successful index regeneration"""
        response = client.post("/api/corpus/regenerate-index")
        assert response.status_code == 200
        
        result = response.json()
        assert result['success'] is True
        assert 'message' in result
        assert 'total_documents' in result
        assert 'research_areas' in result
        assert 'legal_concepts_count' in result
        assert 'last_updated' in result
        
        # Verify the response structure
        assert isinstance(result['total_documents'], int)
        assert isinstance(result['research_areas'], list)
        assert isinstance(result['legal_concepts_count'], int)
        assert result['total_documents'] >= 0
        assert result['legal_concepts_count'] >= 0
    
    def test_regenerate_corpus_index_updates_data(self):
        """Test that corpus index regeneration actually updates the data"""
        # Get initial corpus state
        initial_response = client.get("/api/corpus/")
        assert initial_response.status_code == 200
        initial_items = initial_response.json()
        
        # Regenerate index
        regen_response = client.post("/api/corpus/regenerate-index")
        assert regen_response.status_code == 200
        
        # Get updated corpus state
        updated_response = client.get("/api/corpus/")
        assert updated_response.status_code == 200
        updated_items = updated_response.json()
        
        # Should have same or more items (in case new files were added)
        assert len(updated_items) >= len(initial_items)
        
        # Verify structure is maintained
        for item in updated_items:
            assert 'id' in item
            assert 'title' in item or 'name' in item
            assert 'category' in item
    
    def test_regenerate_corpus_index_updates_categories(self):
        """Test that index regeneration updates category information"""
        # Regenerate index
        regen_response = client.post("/api/corpus/regenerate-index")
        assert regen_response.status_code == 200
        
        # Get categories after regeneration
        categories_response = client.get("/api/corpus/categories")
        assert categories_response.status_code == 200
        
        categories = categories_response.json()
        assert isinstance(categories, dict)
        
        # Should have the main categories
        expected_categories = ['contracts', 'clauses', 'precedents', 'statutes']
        for category in expected_categories:
            if category in categories:  # May not exist if no documents in that category
                assert 'name' in categories[category]
                assert 'description' in categories[category]
                assert 'document_ids' in categories[category]
    
    def test_regenerate_corpus_index_updates_concepts(self):
        """Test that index regeneration updates research concepts"""
        # Regenerate index
        regen_response = client.post("/api/corpus/regenerate-index")
        assert regen_response.status_code == 200
        
        # Get concepts after regeneration
        concepts_response = client.get("/api/corpus/concepts")
        assert concepts_response.status_code == 200
        
        concepts = concepts_response.json()
        assert 'concepts' in concepts
        assert 'total_concepts' in concepts
        assert 'research_areas' in concepts
        
        # Should have research areas from regeneration response
        regen_result = regen_response.json()
        if regen_result['research_areas']:
            assert len(concepts['research_areas']) > 0