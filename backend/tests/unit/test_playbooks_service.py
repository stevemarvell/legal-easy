#!/usr/bin/env python3
"""
Unit tests for PlaybooksService
"""

import pytest
import json
from unittest.mock import patch, mock_open
from pathlib import Path

from app.services.playbooks_service import PlaybooksService


class TestPlaybooksService:
    """Test cases for PlaybooksService"""

    @patch("builtins.open", new_callable=mock_open, read_data='{"playbooks": [{"id": "pb1", "name": "Test Playbook", "case_type": "Employment Dispute"}]}')
    @patch("pathlib.Path.exists", return_value=True)
    def test_load_playbooks_success(self, mock_exists, mock_file):
        """Test loading playbooks successfully"""
        result = PlaybooksService.load_playbooks()
        
        assert len(result) == 1
        assert result[0]["id"] == "pb1"
        assert result[0]["name"] == "Test Playbook"

    @patch("pathlib.Path.exists", return_value=False)
    def test_load_playbooks_file_not_exists(self, mock_exists):
        """Test loading playbooks when file doesn't exist"""
        result = PlaybooksService.load_playbooks()
        
        assert result == []

    @patch("builtins.open", new_callable=mock_open, read_data='{"playbooks": [{"id": "pb1", "case_type": "Employment Dispute"}]}')
    @patch("pathlib.Path.exists", return_value=True)
    def test_match_playbook_success(self, mock_exists, mock_file):
        """Test successful playbook matching"""
        result = PlaybooksService.match_playbook("Employment Dispute")
        
        assert result is not None
        assert result["id"] == "pb1"
        assert result["case_type"] == "Employment Dispute"

    @patch("builtins.open", new_callable=mock_open, read_data='{"playbooks": [{"id": "pb1", "case_type": "Employment Dispute"}]}')
    @patch("pathlib.Path.exists", return_value=True)
    def test_match_playbook_no_match(self, mock_exists, mock_file):
        """Test playbook matching when no match found"""
        result = PlaybooksService.match_playbook("Intellectual Property")
        
        assert result is None

    @patch("builtins.open", new_callable=mock_open, read_data='{"playbooks": [{"id": "pb1", "name": "Test Playbook"}]}')
    @patch("pathlib.Path.exists", return_value=True)
    def test_get_playbook_by_id_success(self, mock_exists, mock_file):
        """Test getting playbook by ID successfully"""
        result = PlaybooksService.get_playbook_by_id("pb1")
        
        assert result is not None
        assert result["id"] == "pb1"
        assert result["name"] == "Test Playbook"

    @patch("builtins.open", new_callable=mock_open, read_data='{"playbooks": [{"id": "pb1", "name": "Test Playbook"}]}')
    @patch("pathlib.Path.exists", return_value=True)
    def test_get_playbook_by_id_not_found(self, mock_exists, mock_file):
        """Test getting playbook by ID when not found"""
        result = PlaybooksService.get_playbook_by_id("nonexistent")
        
        assert result is None

    @patch("app.services.cases_service.CasesService.find_case_by_id")
    def test_analyze_case_with_playbook_case_not_found(self, mock_find_case):
        """Test case analysis when case not found"""
        mock_find_case.return_value = None
        
        result = PlaybooksService.analyze_case_with_playbook("nonexistent")
        
        assert result["case_id"] == "nonexistent"
        assert result["applied_playbook"] is None
        assert "fallback_reason" in result
        assert "Case not found" in result["fallback_reason"]

    @patch("app.services.cases_service.CasesService.find_case_by_id")
    def test_analyze_case_with_playbook_no_case_type(self, mock_find_case):
        """Test case analysis when case has no case_type"""
        mock_case = {"id": "case1", "summary": "Test case"}
        mock_find_case.return_value = mock_case
        
        result = PlaybooksService.analyze_case_with_playbook("case1")
        
        assert "No case type specified" in result["fallback_reason"]

    def test_generate_fallback_analysis(self):
        """Test fallback analysis generation"""
        case_id = "test_case"
        reason = "Test reason"
        
        result = PlaybooksService._generate_fallback_analysis(case_id, reason)
        
        assert result["case_id"] == case_id
        assert result["fallback_reason"] == reason
        assert result["applied_playbook"] is None
        assert result["case_strength_assessment"]["overall_strength"] == "Unknown"
        assert result["case_strength_assessment"]["confidence_level"] == 0.1
        assert len(result["strategic_recommendations"]) > 0
        assert "analysis_timestamp" in result