import pytest
from fastapi.testclient import TestClient
from main import app


class TestLegalResearchAPI:
    """Test cases for Legal Research API endpoints"""
    
    @pytest.fixture
    def client(self):
        """Create test client"""
        return TestClient(app)
    
    def test_search_legal_corpus(self, client):
        """Test POST /legal-research/search endpoint"""
        search_data = {
            "query": "employment contract termination",
            "limit": 5,
            "min_relevance_score": 0.0,
            "sort_by": "relevance"
        }
        
        response = client.post("/legal-research/search", json=search_data)
        
        assert response.status_code == 200
        results = response.json()
        assert isinstance(results, list)
        assert len(results) <= 5
        
        if results:
            result = results[0]
            assert "content" in result
            assert "source_document" in result
            assert "relevance_score" in result
            assert "document_type" in result
            assert "citation" in result
            assert isinstance(result["relevance_score"], float)
            assert result["relevance_score"] >= 0.0
    
    def test_search_with_filters(self, client):
        """Test search with legal area and document type filters"""
        search_data = {
            "query": "contract",
            "limit": 3,
            "legal_area": "Contract Law",
            "document_type": "Legal Clause",
            "sort_by": "relevance"
        }
        
        response = client.post("/legal-research/search", json=search_data)
        
        assert response.status_code == 200
        results = response.json()
        assert isinstance(results, list)
        assert len(results) <= 3
    
    def test_search_with_minimum_relevance(self, client):
        """Test search with minimum relevance score filter"""
        search_data = {
            "query": "employment",
            "limit": 10,
            "min_relevance_score": 0.3,
            "sort_by": "relevance"
        }
        
        response = client.post("/legal-research/search", json=search_data)
        
        assert response.status_code == 200
        results = response.json()
        assert isinstance(results, list)
        
        # All results should have relevance score >= 0.3
        for result in results:
            assert result["relevance_score"] >= 0.3
    
    def test_get_document_categories(self, client):
        """Test GET /legal-research/categories endpoint"""
        response = client.get("/legal-research/categories")
        
        assert response.status_code == 200
        data = response.json()
        assert "categories" in data
        assert "statistics" in data
        assert isinstance(data["categories"], list)
        assert isinstance(data["statistics"], dict)
        
        # Check expected categories
        expected_categories = ["contracts", "clauses", "precedents", "statutes"]
        for category in expected_categories:
            assert category in data["categories"]
        
        # Check statistics structure
        stats = data["statistics"]
        assert "total_documents" in stats
        assert "categories" in stats
        assert isinstance(stats["total_documents"], int)
        assert stats["total_documents"] > 0
    
    def test_search_by_category(self, client):
        """Test POST /legal-research/search/{category} endpoint"""
        search_data = {
            "query": "termination",
            "limit": 5
        }
        
        response = client.post("/legal-research/search/clauses", json=search_data)
        
        assert response.status_code == 200
        results = response.json()
        assert isinstance(results, list)
        assert len(results) <= 5
        
        # Results should be from clauses category
        for result in results:
            assert "Legal Clause" in result["document_type"] or "clause" in result["citation"].lower()
    
    def test_get_relevant_clauses(self, client):
        """Test GET /legal-research/clauses endpoint"""
        response = client.get("/legal-research/clauses?context=employment termination")
        
        assert response.status_code == 200
        data = response.json()
        assert "clauses" in data
        assert isinstance(data["clauses"], list)
        
        if data["clauses"]:
            clause = data["clauses"][0]
            assert "id" in clause
            assert "content" in clause
            assert "source_document" in clause
            assert "legal_area" in clause
            assert "clause_type" in clause
            assert "relevance_score" in clause
    
    def test_get_relevant_clauses_with_legal_area(self, client):
        """Test GET /legal-research/clauses with legal area filter"""
        response = client.get("/legal-research/clauses?context=contract&legal_area=Contract Law")
        
        assert response.status_code == 200
        data = response.json()
        assert "clauses" in data
        assert isinstance(data["clauses"], list)
    
    def test_get_corpus_statistics(self, client):
        """Test GET /legal-research/corpus/stats endpoint"""
        response = client.get("/legal-research/corpus/stats")
        
        assert response.status_code == 200
        stats = response.json()
        assert "total_documents" in stats
        assert "categories" in stats
        assert isinstance(stats["total_documents"], int)
        assert isinstance(stats["categories"], dict)
        assert stats["total_documents"] > 0
    
    def test_get_available_filters(self, client):
        """Test GET /legal-research/filters endpoint"""
        response = client.get("/legal-research/filters")
        
        assert response.status_code == 200
        filters = response.json()
        assert "legal_areas" in filters
        assert "document_types" in filters
        assert "sort_options" in filters
        
        assert isinstance(filters["legal_areas"], list)
        assert isinstance(filters["document_types"], list)
        assert isinstance(filters["sort_options"], list)
        
        # Check expected filter options
        assert "Employment Law" in filters["legal_areas"]
        assert "Contract Law" in filters["legal_areas"]
        assert "Legal Clause" in filters["document_types"]
        assert "relevance" in filters["sort_options"]
    
    def test_search_empty_query(self, client):
        """Test search with empty query"""
        search_data = {
            "query": "",
            "limit": 5
        }
        
        response = client.post("/legal-research/search", json=search_data)
        
        assert response.status_code == 200
        results = response.json()
        assert isinstance(results, list)
        # Empty query should return empty results or handle gracefully
    
    def test_search_invalid_sort_option(self, client):
        """Test search with invalid sort option"""
        search_data = {
            "query": "contract",
            "limit": 5,
            "sort_by": "invalid_sort"
        }
        
        response = client.post("/legal-research/search", json=search_data)
        
        # Should still work, just use default sorting
        assert response.status_code == 200
        results = response.json()
        assert isinstance(results, list)
    
    def test_search_high_limit(self, client):
        """Test search with high limit"""
        search_data = {
            "query": "contract",
            "limit": 100
        }
        
        response = client.post("/legal-research/search", json=search_data)
        
        assert response.status_code == 200
        results = response.json()
        assert isinstance(results, list)
        # Should handle high limits gracefully
        assert len(results) <= 100