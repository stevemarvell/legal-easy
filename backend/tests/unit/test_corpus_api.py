"""
Unit tests for the Corpus API endpoints.

Tests the research corpus API functionality including:
- Browsing corpus items by category
- Getting corpus categories
- Retrieving specific corpus items
- Searching corpus with filters
- Getting research concepts
- Finding related materials
"""

import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from main import app

client = TestClient(app)


class TestCorpusBrowsing:
    """Test corpus browsing endpoints."""

    @patch('app.services.data_service.DataService.search_corpus')
    def test_browse_all_corpus_items(self, mock_search_corpus):
        """Test browsing all corpus items without category filter."""
        # Mock data
        mock_items = [
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
                "id": "rc-004",
                "name": "Termination Clauses",
                "filename": "rc-004_termination_clauses.txt",
                "category": "clauses",
                "document_type": "Research Clause",
                "research_areas": ["Employment Law"],
                "description": "Various termination clause templates"
            }
        ]
        mock_search_corpus.return_value = mock_items

        # Make request
        response = client.get("/api/corpus/")

        # Assertions
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2
        assert data[0]["id"] == "rc-001"
        assert data[0]["category"] == "contracts"
        assert data[1]["id"] == "rc-004"
        assert data[1]["category"] == "clauses"
        mock_search_corpus.assert_called_once_with("")

    @patch('app.services.data_service.DataService.load_corpus_by_category')
    def test_browse_corpus_by_category(self, mock_load_by_category):
        """Test browsing corpus items filtered by category."""
        # Mock data
        mock_items = [
            {
                "id": "rc-001",
                "name": "Employment Contract Template",
                "filename": "rc-001_employment_template.txt",
                "category": "contracts",
                "document_type": "Contract Template",
                "research_areas": ["Employment Law"],
                "description": "Standard UK employment contract template"
            }
        ]
        mock_load_by_category.return_value = mock_items

        # Make request
        response = client.get("/api/corpus/?category=contracts")

        # Assertions
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["category"] == "contracts"
        mock_load_by_category.assert_called_once_with("contracts")

    @patch('app.services.data_service.DataService.search_corpus')
    def test_browse_corpus_error_handling(self, mock_search_corpus):
        """Test error handling in corpus browsing."""
        mock_search_corpus.side_effect = Exception("Database error")

        response = client.get("/api/corpus/")

        assert response.status_code == 500
        assert "Failed to browse corpus" in response.json()["detail"]


class TestCorpusCategories:
    """Test corpus categories endpoint."""

    @patch('app.services.data_service.DataService.load_corpus_categories')
    def test_get_categories_success(self, mock_load_categories):
        """Test successful retrieval of corpus categories."""
        # Mock data
        mock_categories = {
            "contracts": {
                "name": "Contract Templates",
                "description": "Standard UK contract templates",
                "document_ids": ["rc-001", "rc-002", "rc-003"]
            },
            "clauses": {
                "name": "Research Clauses",
                "description": "Library of standard research clauses",
                "document_ids": ["rc-004", "rc-005", "rc-006"]
            }
        }
        mock_load_categories.return_value = mock_categories

        # Make request
        response = client.get("/api/corpus/categories")

        # Assertions
        assert response.status_code == 200
        data = response.json()
        assert "contracts" in data
        assert "clauses" in data
        assert data["contracts"]["name"] == "Contract Templates"
        assert len(data["contracts"]["document_ids"]) == 3

    @patch('app.services.data_service.DataService.load_corpus_categories')
    def test_get_categories_error_handling(self, mock_load_categories):
        """Test error handling in categories endpoint."""
        mock_load_categories.side_effect = Exception("Database error")

        response = client.get("/api/corpus/categories")

        assert response.status_code == 500
        assert "Failed to get categories" in response.json()["detail"]


class TestCorpusItemRetrieval:
    """Test individual corpus item retrieval."""

    @patch('app.services.data_service.DataService.load_corpus_item_by_id')
    def test_get_corpus_item_success(self, mock_load_item):
        """Test successful retrieval of a specific corpus item."""
        # Mock data
        mock_item = {
            "id": "rc-001",
            "name": "Employment Contract Template",
            "filename": "rc-001_employment_template.txt",
            "category": "contracts",
            "document_type": "Contract Template",
            "research_areas": ["Employment Law"],
            "description": "Standard UK employment contract template",
            "content": "EMPLOYMENT AGREEMENT\n\nThis Employment Agreement..."
        }
        mock_load_item.return_value = mock_item

        # Make request
        response = client.get("/api/corpus/rc-001")

        # Assertions
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == "rc-001"
        assert data["name"] == "Employment Contract Template"
        assert "content" in data
        assert data["content"].startswith("EMPLOYMENT AGREEMENT")
        mock_load_item.assert_called_once_with("rc-001")

    @patch('app.services.data_service.DataService.load_corpus_item_by_id')
    def test_get_corpus_item_not_found(self, mock_load_item):
        """Test handling of non-existent corpus item."""
        mock_load_item.return_value = None

        response = client.get("/api/corpus/rc-999")

        assert response.status_code == 404
        assert "Corpus item with ID rc-999 not found" in response.json()["detail"]

    @patch('app.services.data_service.DataService.load_corpus_item_by_id')
    def test_get_corpus_item_error_handling(self, mock_load_item):
        """Test error handling in item retrieval."""
        mock_load_item.side_effect = Exception("Database error")

        response = client.get("/api/corpus/rc-001")

        assert response.status_code == 500
        assert "Failed to get corpus item" in response.json()["detail"]


class TestCorpusSearch:
    """Test corpus search functionality."""

    @patch('app.services.data_service.DataService.search_corpus')
    def test_search_corpus_basic(self, mock_search_corpus):
        """Test basic corpus search functionality."""
        # Mock data
        mock_items = [
            {
                "id": "rc-001",
                "name": "Employment Contract Template",
                "filename": "rc-001_employment_template.txt",
                "category": "contracts",
                "document_type": "Contract Template",
                "research_areas": ["Employment Law"],
                "description": "Standard UK employment contract template"
            }
        ]
        mock_search_corpus.return_value = mock_items

        # Make request
        response = client.get("/api/corpus/search?q=employment")

        # Assertions
        assert response.status_code == 200
        data = response.json()
        assert data["total_count"] == 1
        assert data["query"] == "employment"
        assert len(data["items"]) == 1
        assert data["items"][0]["id"] == "rc-001"
        assert "contracts" in data["categories_found"]
        assert "Employment Law" in data["research_areas_found"]

    @patch('app.services.data_service.DataService.search_corpus')
    def test_search_corpus_with_category_filter(self, mock_search_corpus):
        """Test corpus search with category filtering."""
        # Mock data - includes items from different categories
        mock_items = [
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
                "id": "rc-004",
                "name": "Termination Clauses",
                "filename": "rc-004_termination_clauses.txt",
                "category": "clauses",
                "document_type": "Research Clause",
                "research_areas": ["Employment Law"],
                "description": "Various termination clause templates"
            }
        ]
        mock_search_corpus.return_value = mock_items

        # Make request with category filter
        response = client.get("/api/corpus/search?q=employment&category=contracts")

        # Assertions
        assert response.status_code == 200
        data = response.json()
        assert data["total_count"] == 1  # Only contracts should be returned
        assert data["items"][0]["category"] == "contracts"

    @patch('app.services.data_service.DataService.search_corpus')
    def test_search_corpus_with_research_area_filter(self, mock_search_corpus):
        """Test corpus search with research area filtering."""
        # Mock data
        mock_items = [
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
                "name": "Service Agreement Template",
                "filename": "rc-002_service_agreement.txt",
                "category": "contracts",
                "document_type": "Contract Template",
                "research_areas": ["Commercial Law"],
                "description": "Professional services agreement template"
            }
        ]
        mock_search_corpus.return_value = mock_items

        # Make request with research area filter
        response = client.get("/api/corpus/search?q=contract&research_area=Employment Law")

        # Assertions
        assert response.status_code == 200
        data = response.json()
        assert data["total_count"] == 1  # Only Employment Law items should be returned
        assert "Employment Law" in data["items"][0]["research_areas"]

    @patch('app.services.data_service.DataService.search_corpus')
    def test_search_corpus_error_handling(self, mock_search_corpus):
        """Test error handling in corpus search."""
        mock_search_corpus.side_effect = Exception("Search error")

        response = client.get("/api/corpus/search?q=employment")

        assert response.status_code == 500
        assert "Failed to search corpus" in response.json()["detail"]


class TestResearchConcepts:
    """Test research concepts endpoint."""

    @patch('app.services.data_service.DataService.get_corpus_research_areas')
    @patch('app.services.data_service.DataService.search_corpus')
    @patch('app.services.data_service.DataService.load_corpus_categories')
    def test_get_research_concepts_success(self, mock_load_categories, mock_search_corpus, mock_get_areas):
        """Test successful retrieval of research concepts."""
        # Mock data
        mock_get_areas.return_value = ["Employment Law", "Contract Law"]
        mock_search_corpus.return_value = [
            {"id": "rc-001", "research_areas": ["Employment Law"]},
            {"id": "rc-002", "research_areas": ["Contract Law"]}
        ]
        mock_load_categories.return_value = {"contracts": {}, "clauses": {}}

        # Make request
        response = client.get("/api/corpus/concepts")

        # Assertions
        assert response.status_code == 200
        data = response.json()
        assert data["total_concepts"] == 2
        assert len(data["concepts"]) == 2
        assert data["concepts"][0]["name"] == "Employment Law"
        assert "employment-law" == data["concepts"][0]["id"]
        assert len(data["concepts"][0]["corpus_references"]) > 0

    @patch('app.services.data_service.DataService.get_corpus_research_areas')
    def test_get_research_concepts_error_handling(self, mock_get_areas):
        """Test error handling in research concepts endpoint."""
        mock_get_areas.side_effect = Exception("Database error")

        response = client.get("/api/corpus/concepts")

        assert response.status_code == 500
        assert "Failed to get research concepts" in response.json()["detail"]


class TestRelatedMaterials:
    """Test related materials endpoint."""

    @patch('app.services.data_service.DataService.load_corpus_item_by_id')
    @patch('app.services.data_service.DataService.get_related_corpus_items')
    def test_get_related_materials_success(self, mock_get_related, mock_load_item):
        """Test successful retrieval of related materials."""
        # Mock data
        mock_load_item.return_value = {
            "id": "rc-001",
            "name": "Employment Contract Template",
            "research_areas": ["Employment Law"]
        }
        mock_get_related.return_value = [
            {
                "id": "rc-004",
                "name": "Termination Clauses",
                "filename": "rc-004_termination_clauses.txt",
                "category": "clauses",
                "document_type": "Research Clause",
                "research_areas": ["Employment Law"],
                "description": "Various termination clause templates",
                "relevance_score": 3
            }
        ]

        # Make request
        response = client.get("/api/corpus/rc-001/related")

        # Assertions
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["id"] == "rc-004"
        assert data[0]["relevance_score"] == 3
        mock_load_item.assert_called_once_with("rc-001")
        mock_get_related.assert_called_once_with("rc-001")

    @patch('app.services.data_service.DataService.load_corpus_item_by_id')
    def test_get_related_materials_item_not_found(self, mock_load_item):
        """Test handling of non-existent item in related materials."""
        mock_load_item.return_value = None

        response = client.get("/api/corpus/rc-999/related")

        assert response.status_code == 404
        assert "Corpus item with ID rc-999 not found" in response.json()["detail"]

    @patch('app.services.data_service.DataService.load_corpus_item_by_id')
    @patch('app.services.data_service.DataService.get_related_corpus_items')
    def test_get_related_materials_error_handling(self, mock_get_related, mock_load_item):
        """Test error handling in related materials endpoint."""
        mock_load_item.return_value = {"id": "rc-001"}
        mock_get_related.side_effect = Exception("Database error")

        response = client.get("/api/corpus/rc-001/related")

        assert response.status_code == 500
        assert "Failed to get related materials" in response.json()["detail"]


class TestCorpusAPIIntegration:
    """Integration tests for corpus API endpoints."""

    def test_corpus_api_endpoints_exist(self):
        """Test that all corpus API endpoints are properly registered."""
        # Test that endpoints return proper HTTP methods (not 405 Method Not Allowed)
        endpoints_to_test = [
            ("/api/corpus/", "GET"),
            ("/api/corpus/categories", "GET"),
            ("/api/corpus/search", "GET"),
            ("/api/corpus/concepts", "GET")
        ]

        for endpoint, method in endpoints_to_test:
            if method == "GET":
                # These will fail with 500 due to missing data, but should not be 404 or 405
                response = client.get(endpoint + "?q=test" if "search" in endpoint else endpoint)
                assert response.status_code != 404, f"Endpoint {endpoint} not found"
                assert response.status_code != 405, f"Method {method} not allowed for {endpoint}"

    @patch('app.services.data_service.DataService.search_corpus')
    def test_corpus_response_format_validation(self, mock_search_corpus):
        """Test that API responses match expected Pydantic model formats."""
        # Mock data that matches CorpusItem model
        mock_items = [
            {
                "id": "rc-001",
                "name": "Test Document",
                "filename": "test.txt",
                "category": "contracts",
                "document_type": "Contract Template",
                "research_areas": ["Test Law"],
                "description": "Test description"
            }
        ]
        mock_search_corpus.return_value = mock_items

        response = client.get("/api/corpus/")

        assert response.status_code == 200
        data = response.json()
        
        # Validate response structure matches CorpusItem model
        assert isinstance(data, list)
        item = data[0]
        required_fields = ["id", "name", "filename", "category", "document_type", "research_areas", "description"]
        for field in required_fields:
            assert field in item, f"Required field {field} missing from response"