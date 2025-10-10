"""
Unit tests for DataService corpus-related methods.

Tests the corpus data loading and processing functionality including:
- Loading corpus by category
- Loading corpus categories
- Loading individual corpus items
- Searching corpus
- Getting research areas
- Finding related corpus items
"""

import pytest
from unittest.mock import patch, mock_open, MagicMock
from pathlib import Path
import json
from app.services.data_service import DataService


class TestCorpusDataLoading:
    """Test corpus data loading methods."""

    @patch('app.services.data_service.Path.exists')
    @patch('builtins.open', new_callable=mock_open)
    def test_load_corpus_by_category_success(self, mock_file, mock_exists):
        """Test successful loading of corpus items by category."""
        # Mock file exists
        mock_exists.return_value = True
        
        # Mock corpus data
        mock_corpus_data = {
            "categories": {
                "contracts": {
                    "document_ids": ["rc-001", "rc-002"]
                }
            },
            "documents": {
                "rc-001": {
                    "name": "Employment Contract Template",
                    "category": "contracts",
                    "research_areas": ["Employment Law"]
                },
                "rc-002": {
                    "name": "Service Agreement Template", 
                    "category": "contracts",
                    "research_areas": ["Commercial Law"]
                }
            }
        }
        mock_file.return_value.read.return_value = json.dumps(mock_corpus_data)

        # Test
        result = DataService.load_corpus_by_category("contracts")

        # Assertions
        assert len(result) == 2
        assert result[0]["id"] == "rc-001"
        assert result[0]["name"] == "Employment Contract Template"
        assert result[1]["id"] == "rc-002"
        assert result[1]["name"] == "Service Agreement Template"

    @patch('app.services.data_service.Path.exists')
    def test_load_corpus_by_category_file_not_found(self, mock_exists):
        """Test handling when corpus index file doesn't exist."""
        mock_exists.return_value = False

        result = DataService.load_corpus_by_category("contracts")

        assert result == []

    @patch('app.services.data_service.Path.exists')
    @patch('builtins.open', new_callable=mock_open)
    def test_load_corpus_by_category_invalid_category(self, mock_file, mock_exists):
        """Test handling of invalid category."""
        mock_exists.return_value = True
        mock_corpus_data = {
            "categories": {
                "contracts": {"document_ids": ["rc-001"]}
            },
            "documents": {"rc-001": {"name": "Test"}}
        }
        mock_file.return_value.read.return_value = json.dumps(mock_corpus_data)

        result = DataService.load_corpus_by_category("invalid_category")

        assert result == []

    @patch('app.services.data_service.Path.exists')
    @patch('builtins.open', side_effect=Exception("File read error"))
    def test_load_corpus_by_category_error_handling(self, mock_file, mock_exists):
        """Test error handling in corpus loading."""
        mock_exists.return_value = True

        result = DataService.load_corpus_by_category("contracts")

        assert result == []


class TestCorpusCategories:
    """Test corpus categories loading."""

    @patch('app.services.data_service.Path.exists')
    @patch('builtins.open', new_callable=mock_open)
    def test_load_corpus_categories_success(self, mock_file, mock_exists):
        """Test successful loading of corpus categories."""
        mock_exists.return_value = True
        mock_corpus_data = {
            "categories": {
                "contracts": {
                    "name": "Contract Templates",
                    "description": "Standard UK contract templates",
                    "document_ids": ["rc-001", "rc-002"]
                },
                "clauses": {
                    "name": "Research Clauses",
                    "description": "Library of standard research clauses",
                    "document_ids": ["rc-004", "rc-005"]
                }
            }
        }
        mock_file.return_value.read.return_value = json.dumps(mock_corpus_data)

        result = DataService.load_corpus_categories()

        assert len(result) == 2
        assert "contracts" in result
        assert "clauses" in result
        assert result["contracts"]["name"] == "Contract Templates"
        assert len(result["contracts"]["document_ids"]) == 2

    @patch('app.services.data_service.Path.exists')
    def test_load_corpus_categories_file_not_found(self, mock_exists):
        """Test handling when corpus index file doesn't exist."""
        mock_exists.return_value = False

        result = DataService.load_corpus_categories()

        assert result == {}


class TestCorpusItemById:
    """Test loading individual corpus items."""

    @patch('app.services.data_service.Path.exists')
    @patch('builtins.open', new_callable=mock_open)
    def test_load_corpus_item_by_id_success(self, mock_file, mock_exists):
        """Test successful loading of corpus item with content."""
        # Mock all path exists calls return True
        mock_exists.return_value = True
        
        # Mock corpus index data
        mock_corpus_data = {
            "documents": {
                "rc-001": {
                    "name": "Employment Contract Template",
                    "filename": "rc-001_employment_template.txt",
                    "category": "contracts",
                    "research_areas": ["Employment Law"]
                }
            }
        }
        
        # Mock content file
        mock_content = "EMPLOYMENT AGREEMENT\n\nThis Employment Agreement..."
        
        # Setup mock to return different content based on call order
        mock_file.return_value.__enter__.return_value.read.side_effect = [
            json.dumps(mock_corpus_data),  # First call: index file
            mock_content  # Second call: content file
        ]

        result = DataService.load_corpus_item_by_id("rc-001")

        assert result is not None
        assert result["id"] == "rc-001"
        assert result["name"] == "Employment Contract Template"
        assert result["content"] == mock_content

    @patch('app.services.data_service.Path.exists')
    @patch('builtins.open', new_callable=mock_open)
    def test_load_corpus_item_by_id_not_found(self, mock_file, mock_exists):
        """Test handling when corpus item doesn't exist."""
        mock_exists.return_value = True
        mock_corpus_data = {
            "documents": {
                "rc-001": {"name": "Test Document"}
            }
        }
        mock_file.return_value.read.return_value = json.dumps(mock_corpus_data)

        result = DataService.load_corpus_item_by_id("rc-999")

        assert result is None

    @patch('app.services.data_service.Path.exists')
    def test_load_corpus_item_by_id_file_not_found(self, mock_exists):
        """Test handling when corpus index file doesn't exist."""
        mock_exists.return_value = False

        result = DataService.load_corpus_item_by_id("rc-001")

        assert result is None


class TestCorpusSearch:
    """Test corpus search functionality."""

    @patch('app.services.data_service.Path.exists')
    @patch('builtins.open', new_callable=mock_open)
    def test_search_corpus_with_query(self, mock_file, mock_exists):
        """Test corpus search with query string."""
        mock_exists.return_value = True
        mock_corpus_data = {
            "documents": {
                "rc-001": {
                    "name": "Employment Contract Template",
                    "description": "Standard UK employment contract template",
                    "research_areas": ["Employment Law"]
                },
                "rc-002": {
                    "name": "Service Agreement Template",
                    "description": "Professional services agreement template",
                    "research_areas": ["Commercial Law"]
                }
            }
        }
        mock_file.return_value.read.return_value = json.dumps(mock_corpus_data)

        result = DataService.search_corpus("employment")

        assert len(result) == 1
        assert result[0]["id"] == "rc-001"
        assert result[0]["name"] == "Employment Contract Template"

    @patch('app.services.data_service.Path.exists')
    @patch('builtins.open', new_callable=mock_open)
    def test_search_corpus_empty_query(self, mock_file, mock_exists):
        """Test corpus search with empty query returns all items."""
        mock_exists.return_value = True
        mock_corpus_data = {
            "documents": {
                "rc-001": {"name": "Document 1"},
                "rc-002": {"name": "Document 2"}
            }
        }
        mock_file.return_value.read.return_value = json.dumps(mock_corpus_data)

        result = DataService.search_corpus("")

        assert len(result) == 2
        assert result[0]["id"] == "rc-001"
        assert result[1]["id"] == "rc-002"

    @patch('app.services.data_service.Path.exists')
    @patch('builtins.open', new_callable=mock_open)
    def test_search_corpus_case_insensitive(self, mock_file, mock_exists):
        """Test that corpus search is case insensitive."""
        mock_exists.return_value = True
        mock_corpus_data = {
            "documents": {
                "rc-001": {
                    "name": "Employment Contract Template",
                    "description": "Standard UK employment contract template",
                    "research_areas": ["Employment Law"]
                }
            }
        }
        mock_file.return_value.read.return_value = json.dumps(mock_corpus_data)

        result = DataService.search_corpus("EMPLOYMENT")

        assert len(result) == 1
        assert result[0]["id"] == "rc-001"


class TestCorpusResearchAreas:
    """Test research areas functionality."""

    @patch('app.services.data_service.Path.exists')
    @patch('builtins.open', new_callable=mock_open)
    def test_get_corpus_research_areas_success(self, mock_file, mock_exists):
        """Test successful retrieval of research areas."""
        mock_exists.return_value = True
        mock_corpus_data = {
            "research_areas": [
                "Employment Law",
                "Contract Law",
                "Intellectual Property"
            ]
        }
        mock_file.return_value.read.return_value = json.dumps(mock_corpus_data)

        result = DataService.get_corpus_research_areas()

        assert len(result) == 3
        assert "Employment Law" in result
        assert "Contract Law" in result
        assert "Intellectual Property" in result

    @patch('app.services.data_service.Path.exists')
    def test_get_corpus_research_areas_file_not_found(self, mock_exists):
        """Test handling when corpus index file doesn't exist."""
        mock_exists.return_value = False

        result = DataService.get_corpus_research_areas()

        assert result == []


class TestRelatedCorpusItems:
    """Test related corpus items functionality."""

    @patch('app.services.data_service.DataService.load_corpus_item_by_id')
    @patch('app.services.data_service.Path.exists')
    @patch('builtins.open', new_callable=mock_open)
    def test_get_related_corpus_items_success(self, mock_file, mock_exists, mock_load_item):
        """Test successful retrieval of related corpus items."""
        # Mock the target item
        mock_load_item.return_value = {
            "id": "rc-001",
            "research_areas": ["Employment Law"],
            "category": "contracts"
        }
        
        # Mock corpus data
        mock_exists.return_value = True
        mock_corpus_data = {
            "documents": {
                "rc-001": {
                    "research_areas": ["Employment Law"],
                    "category": "contracts"
                },
                "rc-004": {
                    "research_areas": ["Employment Law"],
                    "category": "clauses"
                },
                "rc-007": {
                    "research_areas": ["Employment Law"],
                    "category": "precedents"
                },
                "rc-002": {
                    "research_areas": ["Commercial Law"],
                    "category": "contracts"
                }
            }
        }
        mock_file.return_value.read.return_value = json.dumps(mock_corpus_data)

        result = DataService.get_related_corpus_items("rc-001")

        # Should return items with shared research areas, sorted by relevance
        assert len(result) > 0
        # Should not include the original item
        assert not any(item["id"] == "rc-001" for item in result)
        # Should include items with shared research areas
        assert any(item["id"] == "rc-004" for item in result)
        assert any(item["id"] == "rc-007" for item in result)

    @patch('app.services.data_service.DataService.load_corpus_item_by_id')
    def test_get_related_corpus_items_item_not_found(self, mock_load_item):
        """Test handling when target item doesn't exist."""
        mock_load_item.return_value = None

        result = DataService.get_related_corpus_items("rc-999")

        assert result == []

    @patch('app.services.data_service.DataService.load_corpus_item_by_id')
    @patch('builtins.open', side_effect=FileNotFoundError("File not found"))
    def test_get_related_corpus_items_corpus_file_not_found(self, mock_open, mock_load_item):
        """Test handling when corpus index file doesn't exist."""
        mock_load_item.return_value = {"id": "rc-001", "research_areas": ["Employment Law"]}

        result = DataService.get_related_corpus_items("rc-001")

        assert result == []


class TestCorpusMetadata:
    """Test corpus metadata functionality."""

    @patch('app.services.data_service.Path.exists')
    @patch('builtins.open', new_callable=mock_open)
    def test_load_corpus_metadata_success(self, mock_file, mock_exists):
        """Test successful loading of corpus metadata."""
        mock_exists.return_value = True
        mock_corpus_data = {
            "corpus_metadata": {
                "version": "1.0",
                "created_date": "2024-01-01",
                "total_documents": 10,
                "research_jurisdiction": "United Kingdom"
            }
        }
        mock_file.return_value.read.return_value = json.dumps(mock_corpus_data)

        result = DataService.load_corpus_metadata()

        assert result["version"] == "1.0"
        assert result["total_documents"] == 10
        assert result["research_jurisdiction"] == "United Kingdom"

    @patch('app.services.data_service.Path.exists')
    def test_load_corpus_metadata_file_not_found(self, mock_exists):
        """Test handling when corpus index file doesn't exist."""
        mock_exists.return_value = False

        result = DataService.load_corpus_metadata()

        assert result == {}


class TestCorpusDataServiceIntegration:
    """Integration tests for corpus data service methods."""

    def test_corpus_methods_error_handling(self):
        """Test that all corpus methods handle errors gracefully."""
        # Test methods that should return empty lists/dicts on error
        methods_and_expected = [
            (DataService.load_corpus_by_category, "contracts", []),
            (DataService.load_corpus_categories, None, {}),
            (DataService.search_corpus, "test", []),
            (DataService.get_corpus_research_areas, None, []),
            (DataService.load_corpus_metadata, None, {}),
            (DataService.get_related_corpus_items, "rc-001", [])
        ]

        for method, arg, expected in methods_and_expected:
            try:
                if arg is not None:
                    result = method(arg)
                else:
                    result = method()
                # Should not raise exception and should return expected empty value
                assert result == expected or isinstance(result, type(expected))
            except Exception as e:
                pytest.fail(f"Method {method.__name__} should handle errors gracefully, but raised: {e}")

    def test_load_corpus_item_by_id_returns_none_on_error(self):
        """Test that load_corpus_item_by_id returns None on error."""
        result = DataService.load_corpus_item_by_id("nonexistent")
        assert result is None