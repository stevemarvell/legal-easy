#!/usr/bin/env python3
"""
Unit tests for CorpusService
"""

import pytest
import json
from unittest.mock import patch, mock_open
from pathlib import Path

from app.services.corpus_service import CorpusService


class TestCorpusService:
    """Test cases for CorpusService"""

    @patch("builtins.open", new_callable=mock_open, read_data='{"corpus_items": [{"id": "item1", "name": "Test Item"}]}')
    @patch("pathlib.Path.exists", return_value=True)
    def test_load_corpus_items_success(self, mock_exists, mock_file):
        """Test loading corpus items successfully"""
        result = CorpusService.load_corpus_items()
        
        assert len(result) == 1
        assert result[0]["id"] == "item1"
        assert result[0]["name"] == "Test Item"

    @patch("pathlib.Path.exists", return_value=False)
    def test_load_corpus_items_file_not_exists(self, mock_exists):
        """Test loading corpus items when file doesn't exist"""
        result = CorpusService.load_corpus_items()
        
        assert result == []

    @patch("builtins.open", new_callable=mock_open, read_data='{"corpus_items": [{"id": "item1", "name": "Employment Law", "description": "employment terms"}]}')
    @patch("pathlib.Path.exists", return_value=True)
    def test_search_corpus_with_query(self, mock_exists, mock_file):
        """Test searching corpus with query"""
        result = CorpusService.search_corpus("employment")
        
        assert len(result) == 1
        assert result[0]["id"] == "item1"

    @patch("builtins.open", new_callable=mock_open, read_data='{"corpus_items": [{"id": "item1", "category": "contracts"}, {"id": "item2", "category": "clauses"}]}')
    @patch("pathlib.Path.exists", return_value=True)
    def test_load_corpus_by_category(self, mock_exists, mock_file):
        """Test loading corpus by category"""
        result = CorpusService.load_corpus_by_category("contracts")
        
        assert len(result) == 1
        assert result[0]["id"] == "item1"
        assert result[0]["category"] == "contracts"

    @patch("builtins.open", new_callable=mock_open, read_data='{"corpus_items": [{"id": "item1", "category": "contracts"}, {"id": "item2", "category": "clauses"}]}')
    @patch("pathlib.Path.exists", return_value=True)
    def test_load_corpus_categories(self, mock_exists, mock_file):
        """Test loading corpus categories"""
        result = CorpusService.load_corpus_categories()
        
        assert "contracts" in result
        assert "clauses" in result
        assert result["contracts"]["name"] == "Contracts"
        assert "item1" in result["contracts"]["document_ids"]

    @patch("builtins.open", new_callable=mock_open)
    @patch("pathlib.Path.exists")
    def test_load_corpus_item_by_id_success(self, mock_exists, mock_file):
        """Test loading corpus item by ID successfully"""
        corpus_data = {
            "corpus_items": [
                {
                    "id": "item1",
                    "name": "Test Document",
                    "file_path": "research_corpus/contracts/test.txt",
                    "category": "contracts"
                }
            ]
        }
        content_data = "Full document content"
        
        def side_effect(path, *args, **kwargs):
            if "research_corpus_index.json" in str(path):
                return mock_open(read_data=json.dumps(corpus_data)).return_value
            else:
                return mock_open(read_data=content_data).return_value
        
        mock_file.side_effect = side_effect
        mock_exists.return_value = True
        
        result = CorpusService.load_corpus_item_by_id("item1")
        
        assert result is not None
        assert result["id"] == "item1"
        assert result["name"] == "Test Document"
        assert result["content"] == content_data

    @patch("builtins.open", new_callable=mock_open, read_data='{"corpus_items": []}')
    @patch("pathlib.Path.exists", return_value=True)
    def test_load_corpus_item_by_id_not_found(self, mock_exists, mock_file):
        """Test loading corpus item by ID when item not found"""
        result = CorpusService.load_corpus_item_by_id("nonexistent")
        
        assert result is None

    @patch("builtins.open", new_callable=mock_open, read_data='{"corpus_items": [{"id": "item1", "research_areas": ["Employment", "Contracts"]}]}')
    @patch("pathlib.Path.exists", return_value=True)
    def test_get_corpus_research_areas(self, mock_exists, mock_file):
        """Test getting corpus research areas"""
        result = CorpusService.get_corpus_research_areas()
        
        assert "Employment" in result
        assert "Contracts" in result

    @patch("builtins.open", new_callable=mock_open, read_data='{"metadata": {"version": "1.0", "last_updated": "2024-01-01"}}')
    @patch("pathlib.Path.exists", return_value=True)
    def test_load_corpus_metadata(self, mock_exists, mock_file):
        """Test loading corpus metadata"""
        result = CorpusService.load_corpus_metadata()
        
        assert result["version"] == "1.0"
        assert result["last_updated"] == "2024-01-01"

    @patch("builtins.open", new_callable=mock_open)
    @patch("pathlib.Path.exists", return_value=True)
    @patch("pathlib.Path.glob")
    @patch("pathlib.Path.mkdir")
    def test_regenerate_corpus_index_success(self, mock_mkdir, mock_glob, mock_exists, mock_file):
        """Test regenerating corpus index successfully"""
        # Mock file discovery with proper absolute paths
        backend_dir = Path(__file__).parent.parent.parent
        test_file = backend_dir / "data" / "research_corpus" / "contracts" / "test.txt"
        mock_glob.return_value = [test_file]
        
        result = CorpusService.regenerate_corpus_index()
        
        assert result is True