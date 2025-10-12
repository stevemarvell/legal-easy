#!/usr/bin/env python3
"""
Unit tests for DocumentsService
"""

import pytest
import json
from unittest.mock import patch, mock_open
from pathlib import Path

from app.services.documents_service import DocumentsService


class TestDocumentsService:
    """Test cases for DocumentsService"""

    @patch("builtins.open", new_callable=mock_open, read_data='[{"id": "doc1", "case_id": "case1"}, {"id": "doc2", "case_id": "case2"}]')
    @patch("pathlib.Path.exists", return_value=True)
    def test_load_case_documents_success(self, mock_exists, mock_file):
        """Test loading case documents for specific case"""
        case_id = "case1"
        
        result = DocumentsService.load_case_documents(case_id)
        
        assert len(result) == 1
        assert result[0]["id"] == "doc1"
        assert result[0]["case_id"] == "case1"

    @patch("pathlib.Path.exists", return_value=False)
    def test_load_case_documents_file_not_exists(self, mock_exists):
        """Test loading case documents when file doesn't exist"""
        result = DocumentsService.load_case_documents("case1")
        
        assert result == []

    @patch("builtins.open", new_callable=mock_open)
    @patch("pathlib.Path.exists")
    def test_load_document_content_success(self, mock_exists, mock_file):
        """Test loading document content successfully"""
        # Mock the index file
        index_data = [
            {
                "id": "doc1",
                "full_content_path": "cases/case_documents/doc1.txt",
                "content_preview": "Preview content"
            }
        ]
        content_data = "Full document content here"
        
        def side_effect(path, *args, **kwargs):
            if "case_documents_index.json" in str(path):
                return mock_open(read_data=json.dumps(index_data)).return_value
            else:
                return mock_open(read_data=content_data).return_value
        
        mock_file.side_effect = side_effect
        mock_exists.return_value = True
        
        result = DocumentsService.load_document_content("doc1")
        
        assert result == content_data

    @patch("builtins.open", new_callable=mock_open)
    @patch("pathlib.Path.exists")
    def test_load_document_content_fallback_to_preview(self, mock_exists, mock_file):
        """Test loading document content falls back to preview when full content not available"""
        index_data = [
            {
                "id": "doc1",
                "content_preview": "Preview content only"
            }
        ]
        
        mock_file.return_value = mock_open(read_data=json.dumps(index_data)).return_value
        # Only the index file exists, not the content file
        mock_exists.return_value = True
        
        result = DocumentsService.load_document_content("doc1")
        
        assert result == "Preview content only"

    @patch("pathlib.Path.exists", return_value=False)
    def test_load_document_content_file_not_exists(self, mock_exists):
        """Test loading document content when file doesn't exist"""
        result = DocumentsService.load_document_content("doc1")
        
        assert result is None

    @patch("builtins.open", new_callable=mock_open, read_data='[{"id": "doc1", "name": "Test Doc"}]')
    @patch("pathlib.Path.exists", return_value=True)
    def test_find_document_by_id_success(self, mock_exists, mock_file):
        """Test finding document by ID successfully"""
        result = DocumentsService.find_document_by_id("doc1")
        
        assert result is not None
        assert result["id"] == "doc1"
        assert result["name"] == "Test Doc"

    @patch("builtins.open", new_callable=mock_open, read_data='[{"id": "doc1", "name": "Test Doc"}]')
    @patch("pathlib.Path.exists", return_value=True)
    def test_find_document_by_id_not_found(self, mock_exists, mock_file):
        """Test finding document by ID when not found"""
        result = DocumentsService.find_document_by_id("nonexistent")
        
        assert result is None

    @patch("builtins.open", side_effect=Exception("File error"))
    @patch("pathlib.Path.exists", return_value=True)
    def test_find_document_by_id_exception(self, mock_exists, mock_file):
        """Test finding document by ID with exception"""
        result = DocumentsService.find_document_by_id("doc1")
        
        assert result is None