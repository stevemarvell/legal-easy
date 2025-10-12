#!/usr/bin/env python3
"""
Unit tests for CasesService
"""

import pytest
import json
from unittest.mock import patch, mock_open
from pathlib import Path

from app.services.cases_service import CasesService


class TestCasesService:
    """Test cases for CasesService"""

    @patch("builtins.open", new_callable=mock_open, read_data='{"cases": [{"id": "case1", "title": "Test Case"}]}')
    @patch("pathlib.Path.exists", return_value=True)
    def test_load_cases_object_format(self, mock_exists, mock_file):
        """Test loading cases from object format"""
        result = CasesService.load_cases()
        
        assert len(result) == 1
        assert result[0]["id"] == "case1"
        assert result[0]["title"] == "Test Case"

    @patch("builtins.open", new_callable=mock_open, read_data='[{"id": "case1", "title": "Test Case"}]')
    @patch("pathlib.Path.exists", return_value=True)
    def test_load_cases_array_format(self, mock_exists, mock_file):
        """Test loading cases from array format"""
        result = CasesService.load_cases()
        
        assert len(result) == 1
        assert result[0]["id"] == "case1"

    @patch("pathlib.Path.exists", return_value=False)
    def test_load_cases_file_not_exists(self, mock_exists):
        """Test loading cases when file doesn't exist"""
        result = CasesService.load_cases()
        
        assert result == []

    @patch("builtins.open", side_effect=Exception("File error"))
    @patch("pathlib.Path.exists", return_value=True)
    def test_load_cases_exception(self, mock_exists, mock_file):
        """Test loading cases with exception"""
        result = CasesService.load_cases()
        
        assert result == []

    @patch("builtins.open", new_callable=mock_open, read_data='[{"id": "case1", "title": "Test Case"}]')
    @patch("pathlib.Path.exists", return_value=True)
    def test_find_case_by_id_success(self, mock_exists, mock_file):
        """Test finding case by ID successfully"""
        result = CasesService.find_case_by_id("case1")
        
        assert result is not None
        assert result["id"] == "case1"
        assert result["title"] == "Test Case"

    @patch("builtins.open", new_callable=mock_open, read_data='[{"id": "case1", "title": "Test Case"}]')
    @patch("pathlib.Path.exists", return_value=True)
    def test_find_case_by_id_not_found(self, mock_exists, mock_file):
        """Test finding case by ID when not found"""
        result = CasesService.find_case_by_id("nonexistent")
        
        assert result is None

    @patch("builtins.open", side_effect=Exception("File error"))
    @patch("pathlib.Path.exists", return_value=True)
    def test_find_case_by_id_exception(self, mock_exists, mock_file):
        """Test finding case by ID with exception"""
        result = CasesService.find_case_by_id("case1")
        
        assert result is None