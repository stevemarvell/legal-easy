#!/usr/bin/env python3
"""
Comprehensive test suite for Corpus API endpoints

This module provides complete test coverage for all corpus-related API endpoints including:
- Corpus browsing and category filtering
- Corpus search functionality
- Research concept analysis
- Individual corpus item retrieval
- Related materials discovery
"""

import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from main import app

client = TestClient(app)


class TestCorpusBrowsing:
    """Test corpus browsing and category functionality"""
    
    def test_browse_corpus_all_items(self):
        """Test browsing all corpus items without category filter"""
        with patch('app.services.data_service.DataService.search_corpus') as mock_search:
            mock_search.return_value = [
                {
                    "id": "rc-001",
                    "name": "Employment Contract Template",
                    "filename": "rc-001_employment_template.txt",
                    "category": "contracts",
                    "document_type": "Contract Template",
                    "research_areas": ["Employment Law"],
                    "description": "Standard UK employment contract template"
                },
                {
                    "id": "rc-002", 
                    "name": "NDA Template",
                    "filename": "rc-002_nda_template.txt",
                    "category": "contracts",
                    "document_type": "Contract Template",
                    "research_areas": ["Contract Law"],
                    "description": "Non-disclosure agreement template"
                }
            ]
            
            response = client.get("/corpus/")
            
            assert response.status_code == 200
            data = response.json()
            assert len(data) == 2
            assert data[0]["id"] == "rc-001"
            assert data[0]["name"] == "Employment Contract Template"
            assert data[0]["category"] == "contracts"
            assert data[1]["id"] == "rc-002"
            mock_search.assert_called_once_with("")
    
    def test_browse_corpus_by_category(self):
        """Test browsing corpus items filtered by category"""
        with patch('app.services.data_service.DataService.load_corpus_by_category') as mock_load:
            mock_load.return_value = [
                {
                    "id": "rc-004",
                    "name": "Termination Clauses",
                    "filename": "rc-004_termination_clauses.txt",
                    "category": "clauses",
                    "document_type": "Legal Clauses",
                    "research_areas": ["Employment Law"],
                    "description": "Various termination clause templates"
                }
            ]
            
            response = client.get("/corpus/?category=clauses")
            
            assert response.status_code == 200
            data = response.json()
            assert len(data) == 1
            assert data[0]["id"] == "rc-004"
            assert data[0]["category"] == "clauses"
            mock_load.assert_called_once_with("clauses")
    
    def test_browse_corpus_empty_category(self):
        """Test browsing corpus with empty category returns empty list"""
        with patch('app.services.data_service.DataService.load_corpus_by_category') as mock_load:
            mock_load.return_value = []
            
            response = client.get("/corpus/?category=nonexistent")
            
            assert response.status_code == 200
            data = response.json()
            assert len(data) == 0
            mock_load.assert_called_once_with("nonexistent")
    
    def test_browse_corpus_service_error(self):
        """Test corpus browsing handles service errors gracefully"""
        with patch('app.services.data_service.DataService.search_corpus') as mock_search:
            mock_search.side_effect = Exception("Database connection failed")
            
            response = client.get("/corpus/")
            
            assert response.status_code == 500
            assert "Failed to browse corpus" in response.json()["detail"]


class TestCorpusCategories:
    """Test corpus categories endpoint"""
    
    def test_get_categories_success(self):
        """Test successful retrieval of corpus categories"""
        with patch('app.services.data_service.DataService.load_corpus_categories') as mock_load:
            mock_load.return_value = {
                "contracts": {
                    "name": "Contract Templates",
                    "description": "Standard UK contract templates",
                    "document_ids": ["rc-001", "rc-002", "rc-003"]
                },
                "clauses": {
                    "name": "Research Clauses", 
                    "description": "Library of standard research clauses",
                    "document_ids": ["rc-004", "rc-005", "rc-006"]
                },
                "precedents": {
                    "name": "Legal Precedents",
                    "description": "Case law and legal precedents",
                    "document_ids": ["rc-007", "rc-008"]
                }
            }
            
            response = client.get("/corpus/categories")
            
            assert response.status_code == 200
            data = response.json()
            assert "contracts" in data
            assert "clauses" in data
            assert "precedents" in data
            assert data["contracts"]["name"] == "Contract Templates"
            assert len(data["contracts"]["document_ids"]) == 3
            assert len(data["clauses"]["document_ids"]) == 3
            assert len(data["precedents"]["document_ids"]) == 2
    
    def test_get_categories_empty(self):
        """Test categories endpoint with no categories"""
        with patch('app.services.data_service.DataService.load_corpus_categories') as mock_load:
            mock_load.return_value = {}
            
            response = client.get("/corpus/categories")
            
            assert response.status_code == 200
            data = response.json()
            assert len(data) == 0
    
    def test_get_categories_service_error(self):
        """Test categories endpoint handles service errors"""
        with patch('app.services.data_service.DataService.load_corpus_categories') as mock_load:
            mock_load.side_effect = Exception("Failed to load categories")
            
            response = client.get("/corpus/categories")
            
            assert response.status_code == 500
            assert "Failed to get categories" in response.json()["detail"]


class TestCorpusSearch:
    """Test corpus search functionality"""
    
    def test_search_corpus_basic(self):
        """Test basic corpus search functionality"""
        with patch('app.services.data_service.DataService.search_corpus') as mock_search:
            mock_search.return_value = [
                {
                    "id": "rc-001",
                    "name": "Employment Contract Template",
                    "category": "contracts",
                    "research_areas": ["Employment Law"],
                    "description": "Standard UK employment contract template"
                },
                {
                    "id": "rc-007",
                    "name": "Employment Rights Case",
                    "category": "precedents", 
                    "research_areas": ["Employment Law"],
                    "description": "Key employment rights precedent"
                }
            ]
            
            response = client.get("/corpus/search?q=employment")
            
            assert response.status_code == 200
            data = response.json()
            assert data["total_count"] == 2
            assert data["query"] == "employment"
            assert len(data["items"]) == 2
            assert "contracts" in data["categories_found"]
            assert "precedents" in data["categories_found"]
            assert "Employment Law" in data["research_areas_found"]
            mock_search.assert_called_once_with("employment")
    
    def test_search_corpus_with_category_filter(self):
        """Test corpus search with category filtering"""
        with patch('app.services.data_service.DataService.search_corpus') as mock_search:
            mock_search.return_value = [
                {
                    "id": "rc-001",
                    "name": "Employment Contract Template",
                    "category": "contracts",
                    "research_areas": ["Employment Law"],
                    "description": "Standard UK employment contract template"
                },
                {
                    "id": "rc-007",
                    "name": "Employment Rights Case",
                    "category": "precedents",
                    "research_areas": ["Employment Law"], 
                    "description": "Key employment rights precedent"
                }
            ]
            
            response = client.get("/corpus/search?q=employment&category=contracts")
            
            assert response.status_code == 200
            data = response.json()
            assert data["total_count"] == 1
            assert data["items"][0]["category"] == "contracts"
            assert "precedents" not in [item["category"] for item in data["items"]]
    
    def test_search_corpus_with_research_area_filter(self):
        """Test corpus search with research area filtering"""
        with patch('app.services.data_service.DataService.search_corpus') as mock_search:
            mock_search.return_value = [
                {
                    "id": "rc-001",
                    "name": "Employment Contract Template",
                    "category": "contracts",
                    "research_areas": ["Employment Law"],
                    "description": "Standard UK employment contract template"
                },
                {
                    "id": "rc-002",
                    "name": "IP License Agreement",
                    "category": "contracts",
                    "research_areas": ["Intellectual Property"],
                    "description": "Intellectual property licensing template"
                }
            ]
            
            response = client.get("/corpus/search?q=contract&research_area=Employment Law")
            
            assert response.status_code == 200
            data = response.json()
            assert data["total_count"] == 1
            assert data["items"][0]["id"] == "rc-001"
            assert "Employment Law" in data["items"][0]["research_areas"]
    
    def test_search_corpus_no_results(self):
        """Test corpus search with no matching results"""
        with patch('app.services.data_service.DataService.search_corpus') as mock_search:
            mock_search.return_value = []
            
            response = client.get("/corpus/search?q=nonexistent")
            
            assert response.status_code == 200
            data = response.json()
            assert data["total_count"] == 0
            assert len(data["items"]) == 0
            assert data["query"] == "nonexistent"
    
    def test_search_corpus_service_error(self):
        """Test corpus search handles service errors"""
        with patch('app.services.data_service.DataService.search_corpus') as mock_search:
            mock_search.side_effect = Exception("Search service unavailable")
            
            response = client.get("/corpus/search?q=test")
            
            assert response.status_code == 500
            assert "Failed to search corpus" in response.json()["detail"]


class TestResearchConcepts:
    """Test research concepts analysis endpoint"""
    
    def test_get_research_concepts_success(self):
        """Test successful retrieval of research concepts"""
        with patch('app.services.data_service.DataService.get_corpus_research_areas') as mock_areas, \
             patch('app.services.data_service.DataService.search_corpus') as mock_search, \
             patch('app.services.data_service.DataService.load_corpus_categories') as mock_categories:
            
            mock_areas.return_value = ["Employment Law", "Contract Law", "Intellectual Property"]
            mock_search.return_value = [
                {"id": "rc-001", "research_areas": ["Employment Law"]},
                {"id": "rc-002", "research_areas": ["Employment Law", "Contract Law"]},
                {"id": "rc-003", "research_areas": ["Intellectual Property"]}
            ]
            mock_categories.return_value = {
                "contracts": {"name": "Contracts"},
                "clauses": {"name": "Clauses"}
            }
            
            response = client.get("/corpus/concepts")
            
            assert response.status_code == 200
            data = response.json()
            assert data["total_concepts"] == 3
            assert len(data["concepts"]) == 3
            assert "Employment Law" in data["research_areas"]
            assert "Contract Law" in data["research_areas"]
            assert "contracts" in data["categories_analyzed"]
            
            # Check concept structure
            employment_concept = next(c for c in data["concepts"] if c["name"] == "Employment Law")
            assert employment_concept["id"] == "employment-law"
            assert len(employment_concept["corpus_references"]) >= 1
    
    def test_get_research_concepts_empty(self):
        """Test research concepts with no data"""
        with patch('app.services.data_service.DataService.get_corpus_research_areas') as mock_areas, \
             patch('app.services.data_service.DataService.search_corpus') as mock_search, \
             patch('app.services.data_service.DataService.load_corpus_categories') as mock_categories:
            
            mock_areas.return_value = []
            mock_search.return_value = []
            mock_categories.return_value = {}
            
            response = client.get("/corpus/concepts")
            
            assert response.status_code == 200
            data = response.json()
            assert data["total_concepts"] == 0
            assert len(data["concepts"]) == 0
    
    def test_get_research_concepts_service_error(self):
        """Test research concepts handles service errors"""
        with patch('app.services.data_service.DataService.get_corpus_research_areas') as mock_areas:
            mock_areas.side_effect = Exception("Failed to load research areas")
            
            response = client.get("/corpus/concepts")
            
            assert response.status_code == 500
            assert "Failed to get research concepts" in response.json()["detail"]


class TestCorpusItemRetrieval:
    """Test individual corpus item retrieval"""
    
    def test_get_corpus_item_success(self):
        """Test successful retrieval of specific corpus item"""
        with patch('app.services.data_service.DataService.load_corpus_item_by_id') as mock_load:
            mock_load.return_value = {
                "id": "rc-001",
                "name": "Employment Contract Template",
                "filename": "rc-001_employment_template.txt",
                "category": "contracts",
                "document_type": "Contract Template",
                "research_areas": ["Employment Law"],
                "description": "Standard UK employment contract template",
                "content": "EMPLOYMENT AGREEMENT\n\nThis Employment Agreement..."
            }
            
            response = client.get("/corpus/rc-001")
            
            assert response.status_code == 200
            data = response.json()
            assert data["id"] == "rc-001"
            assert data["name"] == "Employment Contract Template"
            assert data["category"] == "contracts"
            assert "EMPLOYMENT AGREEMENT" in data["content"]
            mock_load.assert_called_once_with("rc-001")
    
    def test_get_corpus_item_not_found(self):
        """Test corpus item retrieval with non-existent ID"""
        with patch('app.services.data_service.DataService.load_corpus_item_by_id') as mock_load:
            mock_load.return_value = None
            
            response = client.get("/corpus/rc-999")
            
            assert response.status_code == 404
            assert "Corpus item with ID rc-999 not found" in response.json()["detail"]
    
    def test_get_corpus_item_service_error(self):
        """Test corpus item retrieval handles service errors"""
        with patch('app.services.data_service.DataService.load_corpus_item_by_id') as mock_load:
            mock_load.side_effect = Exception("Database error")
            
            response = client.get("/corpus/rc-001")
            
            assert response.status_code == 500
            assert "Failed to get corpus item" in response.json()["detail"]


class TestRelatedMaterials:
    """Test related materials discovery"""
    
    def test_get_related_materials_success(self):
        """Test successful retrieval of related materials"""
        with patch('app.services.data_service.DataService.load_corpus_item_by_id') as mock_load, \
             patch('app.services.data_service.DataService.get_related_corpus_items') as mock_related:
            
            mock_load.return_value = {
                "id": "rc-001",
                "name": "Employment Contract Template",
                "category": "contracts",
                "research_areas": ["Employment Law"]
            }
            mock_related.return_value = [
                {
                    "id": "rc-004",
                    "name": "Termination Clauses",
                    "category": "clauses",
                    "research_areas": ["Employment Law"],
                    "description": "Various termination clause templates",
                    "relevance_score": 3
                },
                {
                    "id": "rc-007",
                    "name": "Employment Rights Case",
                    "category": "precedents",
                    "research_areas": ["Employment Law"],
                    "description": "Key employment rights precedent",
                    "relevance_score": 2
                }
            ]
            
            response = client.get("/corpus/rc-001/related")
            
            assert response.status_code == 200
            data = response.json()
            assert len(data) == 2
            assert data[0]["id"] == "rc-004"
            assert data[0]["category"] == "clauses"
            assert data[1]["id"] == "rc-007"
            assert data[1]["category"] == "precedents"
            mock_load.assert_called_once_with("rc-001")
            mock_related.assert_called_once_with("rc-001")
    
    def test_get_related_materials_item_not_found(self):
        """Test related materials for non-existent corpus item"""
        with patch('app.services.data_service.DataService.load_corpus_item_by_id') as mock_load:
            mock_load.return_value = None
            
            response = client.get("/corpus/rc-999/related")
            
            assert response.status_code == 404
            assert "Corpus item with ID rc-999 not found" in response.json()["detail"]
    
    def test_get_related_materials_empty(self):
        """Test related materials with no related items"""
        with patch('app.services.data_service.DataService.load_corpus_item_by_id') as mock_load, \
             patch('app.services.data_service.DataService.get_related_corpus_items') as mock_related:
            
            mock_load.return_value = {"id": "rc-001", "name": "Test Item"}
            mock_related.return_value = []
            
            response = client.get("/corpus/rc-001/related")
            
            assert response.status_code == 200
            data = response.json()
            assert len(data) == 0
    
    def test_get_related_materials_service_error(self):
        """Test related materials handles service errors"""
        with patch('app.services.data_service.DataService.load_corpus_item_by_id') as mock_load:
            mock_load.side_effect = Exception("Service unavailable")
            
            response = client.get("/corpus/rc-001/related")
            
            assert response.status_code == 500
            assert "Failed to get related materials" in response.json()["detail"]


class TestCorpusIntegration:
    """Integration tests for corpus API endpoints"""
    
    def test_corpus_workflow_integration(self):
        """Test complete corpus workflow from browsing to item retrieval"""
        # Mock all required services
        with patch('app.services.data_service.DataService.search_corpus') as mock_search, \
             patch('app.services.data_service.DataService.load_corpus_item_by_id') as mock_load, \
             patch('app.services.data_service.DataService.get_related_corpus_items') as mock_related:
            
            # Setup mock data
            mock_search.return_value = [
                {
                    "id": "rc-001",
                    "name": "Employment Contract Template",
                    "category": "contracts",
                    "research_areas": ["Employment Law"],
                    "description": "Standard UK employment contract template"
                }
            ]
            
            mock_load.return_value = {
                "id": "rc-001",
                "name": "Employment Contract Template",
                "category": "contracts",
                "research_areas": ["Employment Law"],
                "content": "EMPLOYMENT AGREEMENT\n\nThis Employment Agreement..."
            }
            
            mock_related.return_value = [
                {
                    "id": "rc-004",
                    "name": "Termination Clauses",
                    "category": "clauses",
                    "research_areas": ["Employment Law"]
                }
            ]
            
            # Test workflow: Browse -> Search -> Get Item -> Get Related
            
            # 1. Browse all items
            browse_response = client.get("/corpus/")
            assert browse_response.status_code == 200
            items = browse_response.json()
            assert len(items) == 1
            
            # 2. Search for specific items
            search_response = client.get("/corpus/search?q=employment")
            assert search_response.status_code == 200
            search_data = search_response.json()
            assert search_data["total_count"] == 1
            
            # 3. Get specific item
            item_id = items[0]["id"]
            item_response = client.get(f"/corpus/{item_id}")
            assert item_response.status_code == 200
            item_data = item_response.json()
            assert "content" in item_data
            
            # 4. Get related materials
            related_response = client.get(f"/corpus/{item_id}/related")
            assert related_response.status_code == 200
            related_data = related_response.json()
            assert len(related_data) == 1


if __name__ == "__main__":
    pytest.main([__file__])