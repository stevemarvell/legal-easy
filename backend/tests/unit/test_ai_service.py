#!/usr/bin/env python3
"""
Unit tests for AIService
"""

import pytest
import json
from unittest.mock import patch, mock_open, MagicMock
from pathlib import Path
from datetime import datetime

from app.services.ai_service import AIService


class TestAIService:
    """Test cases for AIService"""

    def test_analyze_document_complete_analysis(self):
        """Test that analyze_document returns complete analysis with all fields"""
        doc_id = "test_doc_1"
        content = """
        Employment Agreement between John Smith and ABC Company Ltd.
        Start date: January 15, 2024
        Termination clause: Either party may terminate with 30 days notice.
        The employee shall maintain confidentiality of all company information.
        """
        
        result = AIService.analyze_document(doc_id, content)
        
        # Check all required fields are present
        assert result["document_id"] == doc_id
        assert "analysis_timestamp" in result
        assert "key_dates" in result
        assert "parties_involved" in result
        assert "document_type" in result
        assert "summary" in result
        assert "key_clauses" in result
        assert "confidence_scores" in result
        assert "overall_confidence" in result
        assert "uncertainty_flags" in result
        assert "risk_level" in result
        assert "potential_issues" in result
        assert "compliance_status" in result
        assert "critical_deadlines" in result
        assert "document_intent" in result
        assert "complexity_score" in result

    def test_extract_dates_various_formats(self):
        """Test date extraction with various date formats"""
        content = """
        Contract dated January 15, 2024
        Due date: 03/20/2024
        Expiry: 2024-12-31
        Meeting on 5th March 2024
        Deadline 12-25-2024
        """
        
        dates = AIService._extract_dates(content)
        
        assert len(dates) > 0
        assert any("2024" in date for date in dates)
        # Should find multiple date formats
        assert len(dates) <= 5  # Limited to 5 dates

    def test_extract_parties_legal_entities(self):
        """Test party extraction from legal document content"""
        content = """
        This agreement is between John Smith and ABC Company Ltd.
        The Employee agrees to work for XYZ Corporation Inc.
        Sarah Johnson will represent the client.
        Tech Solutions LLC provides services.
        """
        
        parties = AIService._extract_parties(content)
        
        assert len(parties) > 0
        # Should find company names
        assert any("Ltd" in party or "Inc" in party or "LLC" in party for party in parties)
        # Should find person names
        assert any(len(party.split()) >= 2 for party in parties)
        # Should be limited to 5 parties
        assert len(parties) <= 5

    def test_extract_parties_filters_false_positives(self):
        """Test that party extraction filters out common false positives"""
        content = """
        This Employment Agreement between The Company and The Employee.
        Either Party may terminate this agreement.
        Such Party shall provide notice.
        """
        
        parties = AIService._extract_parties(content)
        
        # Should filter out generic terms
        false_positives = ['The Company', 'The Employee', 'Either Party', 'Such Party']
        for fp in false_positives:
            assert fp not in parties

    def test_classify_document_type_employment(self):
        """Test document type classification for employment documents"""
        content = "Employment agreement with termination clause for employee"
        
        doc_type = AIService._classify_document_type(content)
        
        assert doc_type == "Employment Document"

    def test_classify_document_type_contract(self):
        """Test document type classification for contracts"""
        content = "Service contract with terms and conditions"
        
        doc_type = AIService._classify_document_type(content)
        
        assert doc_type == "Contract"

    def test_classify_document_type_confidentiality(self):
        """Test document type classification for confidentiality agreements"""
        content = "Non-disclosure confidential information nda"
        
        doc_type = AIService._classify_document_type(content)
        
        assert doc_type == "Confidentiality Agreement"

    def test_generate_summary_short_content(self):
        """Test summary generation with short content"""
        content = "This is a test document. It contains sample text. End of document."
        
        summary = AIService._generate_summary(content)
        
        assert len(summary) > 0
        assert "This is a test document" in summary

    def test_generate_summary_long_content(self):
        """Test summary generation with long content gets truncated"""
        content = "A" * 300 + ". More content here. Even more content."
        
        summary = AIService._generate_summary(content)
        
        assert len(summary) <= 203  # 200 chars + "..."
        if len(summary) > 200:
            assert summary.endswith("...")

    def test_extract_key_clauses(self):
        """Test key clause extraction"""
        content = """
        The parties agree to maintain confidentiality.
        Termination clause: Either party shall provide 30 days notice.
        Payment terms: Company will pay within 30 days.
        """
        
        clauses = AIService._extract_key_clauses(content)
        
        assert len(clauses) <= 5
        # Should find clauses with legal language
        assert any("shall" in clause.lower() or "will" in clause.lower() for clause in clauses)

    def test_calculate_confidence_scores_high_confidence(self):
        """Test confidence score calculation with good data"""
        content = "Long document with good content"
        key_dates = ["2024-01-15", "2024-12-31"]
        parties = ["John Smith", "ABC Company Ltd"]
        doc_type = "Contract"
        summary = "This is a comprehensive summary of the document"
        key_clauses = ["Party shall perform", "Agreement terminates", "Payment due"]
        
        scores = AIService._calculate_confidence_scores(
            content, key_dates, parties, doc_type, summary, key_clauses
        )
        
        assert "dates" in scores
        assert "parties" in scores
        assert "document_type" in scores
        assert "summary" in scores
        assert "key_clauses" in scores
        
        # Should have high confidence with good data
        assert scores["dates"] >= 0.7  # 2 dates
        assert scores["parties"] >= 0.6  # 2 parties
        assert scores["key_clauses"] >= 0.7  # 3 clauses

    def test_calculate_confidence_scores_low_confidence(self):
        """Test confidence score calculation with poor data"""
        content = "Short"
        key_dates = []
        parties = []
        doc_type = "Legal Document"
        summary = "No summary"
        key_clauses = []
        
        scores = AIService._calculate_confidence_scores(
            content, key_dates, parties, doc_type, summary, key_clauses
        )
        
        # Should have low confidence with poor data
        assert scores["dates"] <= 0.5
        assert scores["parties"] <= 0.5
        assert scores["key_clauses"] <= 0.5

    def test_identify_uncertainty_flags(self):
        """Test uncertainty flag identification"""
        confidence_scores = {
            "dates": 0.3,
            "parties": 0.4,
            "document_type": 0.8,
            "summary": 0.6,
            "key_clauses": 0.2
        }
        content = "Short document without clear information"
        
        flags = AIService._identify_uncertainty_flags(confidence_scores, content)
        
        assert len(flags) > 0
        # Should flag low confidence areas
        assert any("dates" in flag for flag in flags)
        assert any("parties" in flag for flag in flags)
        assert any("key_clauses" in flag for flag in flags)

    def test_assess_risk_level_high_risk(self):
        """Test risk level assessment for high risk content"""
        content = "Contract breach and violation with lawsuit damages"
        key_clauses = []
        
        risk_level = AIService._assess_risk_level(content, key_clauses)
        
        assert risk_level == "high"

    def test_assess_risk_level_medium_risk(self):
        """Test risk level assessment for medium risk content"""
        content = "There is a dispute and some concerns about the issue"
        key_clauses = []
        
        risk_level = AIService._assess_risk_level(content, key_clauses)
        
        assert risk_level == "medium"

    def test_assess_risk_level_low_risk(self):
        """Test risk level assessment for low risk content"""
        content = "Agreement shows cooperation and compliance satisfaction"
        key_clauses = []
        
        risk_level = AIService._assess_risk_level(content, key_clauses)
        
        assert risk_level == "low"

    def test_identify_potential_issues(self):
        """Test potential issue identification"""
        content = "Contract breach with unpaid invoices and termination issues"
        key_clauses = []
        
        issues = AIService._identify_potential_issues(content, key_clauses)
        
        assert issues is not None
        assert len(issues) > 0
        assert "Contract breach" in issues
        assert "Payment dispute" in issues
        assert "Termination issues" in issues

    def test_assess_compliance_status_compliant(self):
        """Test compliance status assessment for compliant content"""
        content = "The company is compliant with all regulations"
        doc_type = "Contract"
        
        status = AIService._assess_compliance_status(content, doc_type)
        
        assert status == "Compliant"

    def test_assess_compliance_status_non_compliant(self):
        """Test compliance status assessment for non-compliant content"""
        content = "There was a violation and breach of compliance"
        doc_type = "Contract"
        
        status = AIService._assess_compliance_status(content, doc_type)
        
        assert status == "Non-compliant"

    def test_extract_critical_deadlines(self):
        """Test critical deadline extraction"""
        content = "Payment due by deadline and contract expires soon"
        key_dates = ["2024-01-15", "2024-12-31"]
        
        deadlines = AIService._extract_critical_deadlines(content, key_dates)
        
        assert deadlines is not None
        assert len(deadlines) > 0
        assert all("date" in deadline for deadline in deadlines)
        assert all("type" in deadline for deadline in deadlines)
        assert all("description" in deadline for deadline in deadlines)

    def test_determine_document_intent(self):
        """Test document intent determination"""
        content = "This is a formal agreement between parties"
        doc_type = "Contract"
        
        intent = AIService._determine_document_intent(content, doc_type)
        
        assert intent == "Agreement"

    def test_calculate_complexity_score(self):
        """Test complexity score calculation"""
        content = """
        This is a complex legal document with whereas clauses and heretofore provisions.
        The parties covenant and agree to indemnify each other pursuant to the terms.
        Notwithstanding any other provision, this agreement shall remain in effect.
        """
        
        complexity = AIService._calculate_complexity_score(content)
        
        assert 0.0 <= complexity <= 1.0
        # Should have higher complexity due to legal terms
        assert complexity > 0.1

    @patch("builtins.open", new_callable=mock_open, read_data='{"doc1": {"analysis": "test"}}')
    @patch("pathlib.Path.exists", return_value=True)
    def test_load_existing_analysis_success(self, mock_exists, mock_file):
        """Test loading existing analysis successfully"""
        doc_id = "doc1"
        
        result = AIService.load_existing_analysis(doc_id)
        
        assert result is not None
        assert result == {"analysis": "test"}

    @patch("pathlib.Path.exists", return_value=False)
    def test_load_existing_analysis_file_not_exists(self, mock_exists):
        """Test loading existing analysis when file doesn't exist"""
        doc_id = "doc1"
        
        result = AIService.load_existing_analysis(doc_id)
        
        assert result is None

    @patch("builtins.open", side_effect=Exception("File error"))
    @patch("pathlib.Path.exists", return_value=True)
    def test_load_existing_analysis_exception(self, mock_exists, mock_file):
        """Test loading existing analysis with exception"""
        doc_id = "doc1"
        
        result = AIService.load_existing_analysis(doc_id)
        
        assert result is None

    @patch("builtins.open", new_callable=mock_open, read_data='{}')
    @patch("pathlib.Path.exists", return_value=True)
    @patch("pathlib.Path.mkdir")
    def test_save_analysis_success(self, mock_mkdir, mock_exists, mock_file):
        """Test saving analysis successfully"""
        doc_id = "doc1"
        analysis = {"test": "data"}
        
        # Should not raise exception
        AIService.save_analysis(doc_id, analysis)
        
        # Verify file was written
        mock_file.assert_called()

    @patch("builtins.open", side_effect=Exception("Write error"))
    @patch("pathlib.Path.exists", return_value=True)
    @patch("pathlib.Path.mkdir")
    def test_save_analysis_exception(self, mock_mkdir, mock_exists, mock_file):
        """Test saving analysis with exception"""
        doc_id = "doc1"
        analysis = {"test": "data"}
        
        with pytest.raises(Exception):
            AIService.save_analysis(doc_id, analysis)

    def test_analyze_document_integration(self):
        """Integration test for full document analysis"""
        doc_id = "integration_test"
        content = """
        EMPLOYMENT AGREEMENT
        
        This Employment Agreement is entered into on January 15, 2024, between 
        John Smith (Employee) and Tech Solutions LLC (Company).
        
        TERMINATION: Either party may terminate this agreement with 30 days written notice.
        
        CONFIDENTIALITY: Employee shall maintain confidentiality of all proprietary information.
        
        The parties agree to resolve disputes through arbitration.
        """
        
        result = AIService.analyze_document(doc_id, content)
        
        # Verify comprehensive analysis
        assert result["document_type"] == "Employment Document"
        assert len(result["key_dates"]) > 0
        assert len(result["parties_involved"]) > 0
        assert result["overall_confidence"] > 0
        assert isinstance(result["complexity_score"], float)
        assert result["document_intent"] in ["Agreement", "General correspondence"]