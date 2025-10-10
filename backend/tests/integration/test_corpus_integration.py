"""
Integration tests for the Corpus API.

These tests verify that the corpus API works end-to-end with real data files.
They test the full stack from API endpoints through DataService to actual files.
"""

import pytest
from fastapi.testclient import TestClient
from pathlib import Path
import json
import tempfile
import os
from main import app

client = TestClient(app)


@pytest.fixture
def temp_corpus_data():
    """Create temporary corpus data for testing."""
    # Create temporary directory structure
    temp_dir = tempfile.mkdtemp()
    corpus_dir = Path(temp_dir) / "research_corpus"
    corpus_dir.mkdir()
    
    # Create subdirectories
    for subdir in ["contracts", "clauses", "precedents", "statutes"]:
        (corpus_dir / subdir).mkdir()
    
    # Create test corpus index
    corpus_index = {
        "corpus_metadata": {
            "version": "1.0",
            "created_date": "2024-01-01",
            "total_documents": 2,
            "research_jurisdiction": "United Kingdom"
        },
        "documents": {
            "rc-001": {
                "id": "rc-001",
                "name": "Test Employment Contract",
                "filename": "rc-001_test_employment.txt",
                "category": "contracts",
                "document_type": "Contract Template",
                "research_areas": ["Employment Law"],
                "description": "Test employment contract template"
            },
            "rc-004": {
                "id": "rc-004",
                "name": "Test Termination Clause",
                "filename": "rc-004_test_termination.txt",
                "category": "clauses",
                "document_type": "Research Clause",
                "research_areas": ["Employment Law"],
                "description": "Test termination clause"
            }
        },
        "categories": {
            "contracts": {
                "name": "Contract Templates",
                "description": "Test contract templates",
                "document_ids": ["rc-001"]
            },
            "clauses": {
                "name": "Research Clauses",
                "description": "Test research clauses",
                "document_ids": ["rc-004"]
            }
        },
        "research_areas": ["Employment Law"],
        "document_types": ["Contract Template", "Research Clause"]
    }
    
    # Write corpus index file
    with open(corpus_dir / "research_corpus_index.json", "w") as f:
        json.dump(corpus_index, f, indent=2)
    
    # Create test content files
    with open(corpus_dir / "contracts" / "rc-001_test_employment.txt", "w") as f:
        f.write("TEST EMPLOYMENT AGREEMENT\n\nThis is a test employment contract...")
    
    with open(corpus_dir / "clauses" / "rc-004_test_termination.txt", "w") as f:
        f.write("TERMINATION CLAUSE\n\nThis clause governs termination...")
    
    return temp_dir


class TestCorpusIntegration:
    """Integration tests for corpus API with real data."""

    def test_corpus_api_with_real_data_structure(self):
        """Test corpus API endpoints with the actual data structure."""
        # This test uses the real research_corpus data if it exists
        corpus_path = Path("data/research_corpus/research_corpus_index.json")
        
        if not corpus_path.exists():
            pytest.skip("Real corpus data not available")
        
        # Test browsing all items
        response = client.get("/api/corpus/")
        assert response.status_code == 200
        items = response.json()
        assert isinstance(items, list)
        
        if len(items) > 0:
            # Test getting categories
            response = client.get("/api/corpus/categories")
            assert response.status_code == 200
            categories = response.json()
            assert isinstance(categories, dict)
            
            # Test getting specific item
            first_item_id = items[0]["id"]
            response = client.get(f"/api/corpus/{first_item_id}")
            assert response.status_code == 200
            item = response.json()
            assert item["id"] == first_item_id
            
            # Test search
            response = client.get("/api/corpus/search?q=employment")
            assert response.status_code == 200
            search_result = response.json()
            assert "items" in search_result
            assert "total_count" in search_result

    def test_corpus_api_error_handling_with_missing_data(self):
        """Test API error handling when data files are missing."""
        # Test getting non-existent item
        response = client.get("/api/corpus/nonexistent-item")
        assert response.status_code == 404
        assert "not found" in response.json()["detail"].lower()

    def test_corpus_search_functionality(self):
        """Test search functionality with various queries."""
        test_queries = [
            ("employment", 200),
            ("contract", 200),
            ("nonexistent_term_12345", 200),  # Should return empty results, not error
            ("", 200)  # Empty query should return all items
        ]
        
        for query, expected_status in test_queries:
            response = client.get(f"/api/corpus/search?q={query}")
            assert response.status_code == expected_status
            
            if expected_status == 200:
                data = response.json()
                assert "items" in data
                assert "total_count" in data
                assert "query" in data
                assert data["query"] == query

    def test_corpus_category_filtering(self):
        """Test category filtering functionality."""
        # Test browsing by category
        categories = ["contracts", "clauses", "precedents", "statutes"]
        
        for category in categories:
            response = client.get(f"/api/corpus/?category={category}")
            assert response.status_code == 200
            items = response.json()
            assert isinstance(items, list)
            
            # If items exist, they should all be from the requested category
            for item in items:
                assert item["category"] == category

    def test_research_concepts_endpoint(self):
        """Test research concepts endpoint functionality."""
        response = client.get("/api/corpus/concepts")
        assert response.status_code == 200
        
        data = response.json()
        assert "concepts" in data
        assert "total_concepts" in data
        assert "categories_analyzed" in data
        assert "research_areas" in data
        
        # Validate concept structure
        for concept in data["concepts"]:
            assert "id" in concept
            assert "name" in concept
            assert "definition" in concept
            assert "related_concepts" in concept
            assert "corpus_references" in concept

    def test_related_materials_functionality(self):
        """Test related materials endpoint."""
        # First get an item to test with
        response = client.get("/api/corpus/")
        assert response.status_code == 200
        items = response.json()
        
        if len(items) > 0:
            item_id = items[0]["id"]
            
            # Test getting related materials
            response = client.get(f"/api/corpus/{item_id}/related")
            assert response.status_code == 200
            related_items = response.json()
            assert isinstance(related_items, list)
            
            # Related items should not include the original item
            for related_item in related_items:
                assert related_item["id"] != item_id

    def test_api_response_formats(self):
        """Test that API responses match expected formats."""
        # Test corpus item format
        response = client.get("/api/corpus/")
        if response.status_code == 200:
            items = response.json()
            if len(items) > 0:
                item = items[0]
                required_fields = [
                    "id", "name", "filename", "category", 
                    "document_type", "research_areas", "description"
                ]
                for field in required_fields:
                    assert field in item, f"Missing required field: {field}"

        # Test search result format
        response = client.get("/api/corpus/search?q=test")
        if response.status_code == 200:
            data = response.json()
            required_fields = [
                "items", "total_count", "query", 
                "categories_found", "research_areas_found"
            ]
            for field in required_fields:
                assert field in data, f"Missing required field: {field}"

        # Test categories format
        response = client.get("/api/corpus/categories")
        if response.status_code == 200:
            categories = response.json()
            for category_id, category_data in categories.items():
                required_fields = ["name", "description", "document_ids"]
                for field in required_fields:
                    assert field in category_data, f"Missing required field: {field}"


class TestCorpusDataConsistency:
    """Test data consistency and integrity."""

    def test_corpus_data_integrity(self):
        """Test that corpus data is internally consistent."""
        # Get all items
        response = client.get("/api/corpus/")
        if response.status_code != 200:
            pytest.skip("Corpus data not available")
        
        items = response.json()
        if len(items) == 0:
            pytest.skip("No corpus items available")
        
        # Get categories
        response = client.get("/api/corpus/categories")
        assert response.status_code == 200
        categories = response.json()
        
        # Check that all items belong to valid categories
        valid_categories = set(categories.keys())
        for item in items:
            assert item["category"] in valid_categories, f"Invalid category: {item['category']}"
        
        # Check that category document_ids reference existing items
        item_ids = {item["id"] for item in items}
        for category_id, category_data in categories.items():
            for doc_id in category_data["document_ids"]:
                assert doc_id in item_ids, f"Category {category_id} references non-existent item: {doc_id}"

    def test_search_consistency(self):
        """Test that search results are consistent."""
        # Search for a term and verify results
        response = client.get("/api/corpus/search?q=employment")
        if response.status_code == 200:
            data = response.json()
            
            # Total count should match items length
            assert data["total_count"] == len(data["items"])
            
            # Categories found should match items' categories
            item_categories = {item["category"] for item in data["items"]}
            assert set(data["categories_found"]) == item_categories
            
            # Research areas found should match items' research areas
            item_research_areas = set()
            for item in data["items"]:
                item_research_areas.update(item["research_areas"])
            assert set(data["research_areas_found"]) == item_research_areas


class TestCorpusPerformance:
    """Basic performance tests for corpus API."""

    def test_api_response_times(self):
        """Test that API responses are reasonably fast."""
        import time
        
        endpoints = [
            "/api/corpus/",
            "/api/corpus/categories",
            "/api/corpus/search?q=test",
            "/api/corpus/concepts"
        ]
        
        for endpoint in endpoints:
            start_time = time.time()
            response = client.get(endpoint)
            end_time = time.time()
            
            response_time = end_time - start_time
            
            # API should respond within 5 seconds (generous for testing)
            assert response_time < 5.0, f"Endpoint {endpoint} took {response_time:.2f}s"
            
            # If successful, should be much faster (under 1 second)
            if response.status_code == 200:
                assert response_time < 1.0, f"Successful endpoint {endpoint} took {response_time:.2f}s"