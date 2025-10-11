#!/usr/bin/env python3
"""
Comprehensive test suite for Documentation API endpoints

This module provides complete test coverage for all documentation-related API endpoints including:
- Documentation categories and overview
- Documentation search functionality
- JSON schemas retrieval
- Category-specific documentation access
"""

import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from main import app

client = TestClient(app)


class TestDocumentationOverview:
    """Test documentation categories and overview functionality"""
    
    def test_get_documentation_categories_success(self):
        """Test successful retrieval of documentation categories"""
        with patch('app.services.data_service.DataService.load_documentation_categories') as mock_categories, \
             patch('app.services.data_service.DataService.get_all_documentation_tags') as mock_tags:
            
            mock_categories.return_value = {
                "api": {
                    "name": "API Documentation",
                    "description": "Complete API reference and examples",
                    "document_ids": ["api-overview", "api-examples", "api-reference"]
                },
                "architecture": {
                    "name": "System Architecture",
                    "description": "System design and architecture documentation",
                    "document_ids": ["arch-overview", "data-models"]
                },
                "deployment": {
                    "name": "Deployment Guide",
                    "description": "Deployment and configuration guides",
                    "document_ids": ["deploy-guide"]
                }
            }
            mock_tags.return_value = ["api", "reference", "examples", "architecture", "deployment"]
            
            response = client.get("/docs/")
            
            assert response.status_code == 200
            data = response.json()
            assert "categories" in data
            assert "total_documents" in data
            assert "available_tags" in data
            assert "last_updated" in data
            
            # Check categories structure
            assert "api" in data["categories"]
            assert "architecture" in data["categories"]
            assert "deployment" in data["categories"]
            assert data["categories"]["api"]["name"] == "API Documentation"
            assert len(data["categories"]["api"]["document_ids"]) == 3
            
            # Check totals
            assert data["total_documents"] == 6  # 3 + 2 + 1
            assert len(data["available_tags"]) == 5
    
    def test_get_documentation_categories_empty(self):
        """Test documentation categories with no categories"""
        with patch('app.services.data_service.DataService.load_documentation_categories') as mock_categories, \
             patch('app.services.data_service.DataService.get_all_documentation_tags') as mock_tags:
            
            mock_categories.return_value = {}
            mock_tags.return_value = []
            
            response = client.get("/docs/")
            
            assert response.status_code == 200
            data = response.json()
            assert len(data["categories"]) == 0
            assert data["total_documents"] == 0
            assert len(data["available_tags"]) == 0
    
    def test_get_documentation_categories_service_error(self):
        """Test documentation categories handles service errors"""
        with patch('app.services.data_service.DataService.load_documentation_categories') as mock_categories:
            mock_categories.side_effect = Exception("Database connection failed")
            
            response = client.get("/docs/")
            
            assert response.status_code == 500
            assert "Failed to get documentation categories" in response.json()["detail"]


class TestDocumentationSearch:
    """Test documentation search functionality"""
    
    def test_search_documentation_basic(self):
        """Test basic documentation search functionality"""
        with patch('app.services.data_service.DataService.search_documentation') as mock_search:
            mock_search.return_value = [
                {
                    "id": "api-overview",
                    "name": "API Overview",
                    "category": "api",
                    "description": "Complete API overview and getting started guide",
                    "tags": ["api", "reference", "getting-started"]
                },
                {
                    "id": "api-examples",
                    "name": "API Examples",
                    "category": "api",
                    "description": "Practical API usage examples",
                    "tags": ["api", "examples", "tutorial"]
                }
            ]
            
            response = client.get("/docs/search?q=api")
            
            assert response.status_code == 200
            data = response.json()
            assert data["total_count"] == 2
            assert data["query"] == "api"
            assert len(data["items"]) == 2
            assert data["items"][0]["id"] == "api-overview"
            assert data["items"][1]["id"] == "api-examples"
            assert "api" in data["categories_found"]
            assert "api" in data["tags_found"]
            assert "reference" in data["tags_found"]
            mock_search.assert_called_once_with("api")
    
    def test_search_documentation_with_category_filter(self):
        """Test documentation search with category filtering"""
        with patch('app.services.data_service.DataService.search_documentation') as mock_search:
            mock_search.return_value = [
                {
                    "id": "api-overview",
                    "name": "API Overview",
                    "category": "api",
                    "description": "Complete API overview",
                    "tags": ["api", "reference"]
                },
                {
                    "id": "arch-overview",
                    "name": "Architecture Overview",
                    "category": "architecture",
                    "description": "System architecture overview",
                    "tags": ["architecture", "design"]
                }
            ]
            
            response = client.get("/docs/search?q=overview&category=api")
            
            assert response.status_code == 200
            data = response.json()
            assert data["total_count"] == 1
            assert data["items"][0]["category"] == "api"
            assert data["items"][0]["id"] == "api-overview"
    
    def test_search_documentation_with_tag_filter(self):
        """Test documentation search with tag filtering"""
        with patch('app.services.data_service.DataService.search_documentation') as mock_search:
            mock_search.return_value = [
                {
                    "id": "api-overview",
                    "name": "API Overview",
                    "category": "api",
                    "description": "Complete API overview",
                    "tags": ["api", "reference"]
                },
                {
                    "id": "api-examples",
                    "name": "API Examples",
                    "category": "api",
                    "description": "API usage examples",
                    "tags": ["api", "examples"]
                }
            ]
            
            response = client.get("/docs/search?q=api&tag=reference")
            
            assert response.status_code == 200
            data = response.json()
            assert data["total_count"] == 1
            assert data["items"][0]["id"] == "api-overview"
            assert "reference" in data["items"][0]["tags"]
    
    def test_search_documentation_no_results(self):
        """Test documentation search with no matching results"""
        with patch('app.services.data_service.DataService.search_documentation') as mock_search:
            mock_search.return_value = []
            
            response = client.get("/docs/search?q=nonexistent")
            
            assert response.status_code == 200
            data = response.json()
            assert data["total_count"] == 0
            assert len(data["items"]) == 0
            assert data["query"] == "nonexistent"
            assert len(data["categories_found"]) == 0
            assert len(data["tags_found"]) == 0
    
    def test_search_documentation_service_error(self):
        """Test documentation search handles service errors"""
        with patch('app.services.data_service.DataService.search_documentation') as mock_search:
            mock_search.side_effect = Exception("Search service unavailable")
            
            response = client.get("/docs/search?q=test")
            
            assert response.status_code == 500
            assert "Failed to search documentation" in response.json()["detail"]


class TestJSONSchemas:
    """Test JSON schemas retrieval functionality"""
    
    def test_get_json_schemas_success(self):
        """Test successful retrieval of JSON schemas"""
        with patch('app.services.data_service.DataService.load_json_schemas') as mock_schemas:
            mock_schemas.return_value = {
                "Case": {
                    "type": "object",
                    "properties": {
                        "id": {"type": "string"},
                        "title": {"type": "string"},
                        "case_type": {"type": "string"},
                        "status": {"type": "string"}
                    },
                    "required": ["id", "title", "case_type"]
                },
                "Document": {
                    "type": "object",
                    "properties": {
                        "id": {"type": "string"},
                        "name": {"type": "string"},
                        "type": {"type": "string"},
                        "size": {"type": "integer"}
                    },
                    "required": ["id", "name"]
                },
                "CorpusItem": {
                    "type": "object",
                    "properties": {
                        "id": {"type": "string"},
                        "name": {"type": "string"},
                        "category": {"type": "string"}
                    }
                }
            }
            
            response = client.get("/docs/schemas")
            
            assert response.status_code == 200
            data = response.json()
            assert "schemas" in data
            assert "total_count" in data
            assert "categories" in data
            
            assert data["total_count"] == 3
            assert len(data["schemas"]) == 3
            assert "api" in data["categories"]
            assert "data-models" in data["categories"]
            
            # Check schema structure
            case_schema = next(s for s in data["schemas"] if s["name"] == "Case")
            assert case_schema["description"] == "JSON schema for Case data model"
            assert "properties" in case_schema["schema_definition"]
            assert "id" in case_schema["schema_definition"]["properties"]
    
    def test_get_json_schemas_empty(self):
        """Test JSON schemas with no schemas available"""
        with patch('app.services.data_service.DataService.load_json_schemas') as mock_schemas:
            mock_schemas.return_value = {}
            
            response = client.get("/docs/schemas")
            
            assert response.status_code == 200
            data = response.json()
            assert data["total_count"] == 0
            assert len(data["schemas"]) == 0
    
    def test_get_json_schemas_service_error(self):
        """Test JSON schemas handles service errors"""
        with patch('app.services.data_service.DataService.load_json_schemas') as mock_schemas:
            mock_schemas.side_effect = Exception("Schema loading failed")
            
            response = client.get("/docs/schemas")
            
            assert response.status_code == 500
            assert "Failed to get JSON schemas" in response.json()["detail"]


class TestDocumentationByCategory:
    """Test category-specific documentation retrieval"""
    
    def test_get_documentation_by_category_success(self):
        """Test successful retrieval of documentation by category"""
        with patch('app.services.data_service.DataService.load_documentation_categories') as mock_categories, \
             patch('app.services.data_service.DataService.load_documentation_by_category') as mock_by_category, \
             patch('app.services.data_service.DataService.load_documentation_item_by_id') as mock_by_id:
            
            mock_categories.return_value = {
                "api": {
                    "name": "API Documentation",
                    "description": "Complete API reference",
                    "document_ids": ["api-overview", "api-examples"]
                }
            }
            
            mock_by_category.return_value = [
                {
                    "id": "api-overview",
                    "name": "API Overview",
                    "category": "api",
                    "description": "Complete API overview"
                },
                {
                    "id": "api-examples",
                    "name": "API Examples",
                    "category": "api",
                    "description": "Practical API examples"
                }
            ]
            
            mock_by_id.side_effect = [
                {
                    "id": "api-overview",
                    "name": "API Overview",
                    "filename": "README.md",
                    "category": "api",
                    "document_type": "API Reference",
                    "description": "Complete API overview and getting started guide",
                    "tags": ["api", "reference", "getting-started"],
                    "content": "# API Overview\n\nWelcome to the API..."
                },
                {
                    "id": "api-examples",
                    "name": "API Examples",
                    "filename": "examples.md",
                    "category": "api",
                    "document_type": "Examples",
                    "description": "Practical API usage examples",
                    "tags": ["api", "examples", "tutorial"],
                    "content": "# API Examples\n\nHere are some examples..."
                }
            ]
            
            response = client.get("/docs/api")
            
            assert response.status_code == 200
            data = response.json()
            assert len(data) == 2
            assert data[0]["id"] == "api-overview"
            assert data[0]["category"] == "api"
            assert "content" in data[0]
            assert data[1]["id"] == "api-examples"
            assert "API Examples" in data[1]["content"]
    
    def test_get_documentation_by_category_not_found(self):
        """Test documentation by category with invalid category"""
        with patch('app.services.data_service.DataService.load_documentation_categories') as mock_categories:
            mock_categories.return_value = {
                "api": {"name": "API Documentation"}
            }
            
            response = client.get("/docs/invalid-category")
            
            assert response.status_code == 404
            assert "Documentation category 'invalid-category' not found" in response.json()["detail"]
    
    def test_get_documentation_by_category_empty(self):
        """Test documentation by category with no documents"""
        with patch('app.services.data_service.DataService.load_documentation_categories') as mock_categories, \
             patch('app.services.data_service.DataService.load_documentation_by_category') as mock_by_category:
            
            mock_categories.return_value = {
                "api": {"name": "API Documentation"}
            }
            mock_by_category.return_value = []
            
            response = client.get("/docs/api")
            
            assert response.status_code == 200
            data = response.json()
            assert len(data) == 0
    
    def test_get_documentation_by_category_partial_content_load(self):
        """Test documentation by category with some content loading failures"""
        with patch('app.services.data_service.DataService.load_documentation_categories') as mock_categories, \
             patch('app.services.data_service.DataService.load_documentation_by_category') as mock_by_category, \
             patch('app.services.data_service.DataService.load_documentation_item_by_id') as mock_by_id:
            
            mock_categories.return_value = {
                "api": {"name": "API Documentation"}
            }
            
            mock_by_category.return_value = [
                {
                    "id": "api-overview",
                    "name": "API Overview",
                    "category": "api"
                },
                {
                    "id": "api-examples",
                    "name": "API Examples",
                    "category": "api"
                }
            ]
            
            # First call returns full content, second returns None
            mock_by_id.side_effect = [
                {
                    "id": "api-overview",
                    "name": "API Overview",
                    "content": "Full content here"
                },
                None  # Simulates content loading failure
            ]
            
            response = client.get("/docs/api")
            
            assert response.status_code == 200
            data = response.json()
            assert len(data) == 2
            assert "content" in data[0]  # First item has full content
            assert "content" not in data[1]  # Second item falls back to basic info
    
    def test_get_documentation_by_category_service_error(self):
        """Test documentation by category handles service errors"""
        with patch('app.services.data_service.DataService.load_documentation_categories') as mock_categories:
            mock_categories.side_effect = Exception("Service unavailable")
            
            response = client.get("/docs/api")
            
            assert response.status_code == 500
            assert "Failed to get documentation by category" in response.json()["detail"]


class TestDocumentationIntegration:
    """Integration tests for documentation API endpoints"""
    
    def test_documentation_workflow_integration(self):
        """Test complete documentation workflow from overview to specific content"""
        # Mock all required services
        with patch('app.services.data_service.DataService.load_documentation_categories') as mock_categories, \
             patch('app.services.data_service.DataService.get_all_documentation_tags') as mock_tags, \
             patch('app.services.data_service.DataService.search_documentation') as mock_search, \
             patch('app.services.data_service.DataService.load_documentation_by_category') as mock_by_category, \
             patch('app.services.data_service.DataService.load_documentation_item_by_id') as mock_by_id:
            
            # Setup mock data
            mock_categories.return_value = {
                "api": {
                    "name": "API Documentation",
                    "description": "Complete API reference",
                    "document_ids": ["api-overview"]
                }
            }
            mock_tags.return_value = ["api", "reference"]
            
            mock_search.return_value = [
                {
                    "id": "api-overview",
                    "name": "API Overview",
                    "category": "api",
                    "description": "Complete API overview",
                    "tags": ["api", "reference"]
                }
            ]
            
            mock_by_category.return_value = [
                {
                    "id": "api-overview",
                    "name": "API Overview",
                    "category": "api"
                }
            ]
            
            mock_by_id.return_value = {
                "id": "api-overview",
                "name": "API Overview",
                "content": "# API Overview\n\nComplete API documentation..."
            }
            
            # Test workflow: Overview -> Search -> Category -> Content
            
            # 1. Get documentation overview
            overview_response = client.get("/docs/")
            assert overview_response.status_code == 200
            overview_data = overview_response.json()
            assert "api" in overview_data["categories"]
            
            # 2. Search documentation
            search_response = client.get("/docs/search?q=api")
            assert search_response.status_code == 200
            search_data = search_response.json()
            assert search_data["total_count"] == 1
            
            # 3. Get category-specific documentation
            category_response = client.get("/docs/api")
            assert category_response.status_code == 200
            category_data = category_response.json()
            assert len(category_data) == 1
            assert "content" in category_data[0]
    
    def test_documentation_error_handling_integration(self):
        """Test documentation API error handling across endpoints"""
        # Test cascading error handling
        with patch('app.services.data_service.DataService.load_documentation_categories') as mock_categories:
            mock_categories.side_effect = Exception("Service down")
            
            # All endpoints should handle the service error gracefully
            overview_response = client.get("/docs/")
            assert overview_response.status_code == 500
            
            category_response = client.get("/docs/api")
            assert category_response.status_code == 500
            
            # Search should still work if it uses a different service
            with patch('app.services.data_service.DataService.search_documentation') as mock_search:
                mock_search.return_value = []
                search_response = client.get("/docs/search?q=test")
                assert search_response.status_code == 200


if __name__ == "__main__":
    pytest.main([__file__])