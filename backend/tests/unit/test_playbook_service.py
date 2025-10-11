#!/usr/bin/env python3
"""
Unit tests for PlaybookService
"""

import pytest
import json
from unittest.mock import patch, mock_open, MagicMock
from pathlib import Path
from datetime import datetime

from app.services.playbook_service import PlaybookService


class TestPlaybookService:
    """Test cases for PlaybookService"""

    @patch("builtins.open", new_callable=mock_open)
    @patch("pathlib.Path.exists", return_value=True)
    def test_match_playbook_success(self, mock_exists, mock_file):
        """Test successful playbook matching"""
        playbooks_data = {
            "playbooks": [
                {"id": "pb1", "name": "Employment Playbook", "case_type": "Employment Dispute"},
                {"id": "pb2", "name": "Contract Playbook", "case_type": "Contract Breach"}
            ]
        }
        
        mock_file.return_value = mock_open(read_data=json.dumps(playbooks_data)).return_value
        
        result = PlaybookService.match_playbook("Employment Dispute")
        
        assert result is not None
        assert result["id"] == "pb1"
        assert result["case_type"] == "Employment Dispute"

    @patch("builtins.open", new_callable=mock_open)
    @patch("pathlib.Path.exists", return_value=True)
    def test_match_playbook_array_format(self, mock_exists, mock_file):
        """Test playbook matching with array format"""
        playbooks_data = [
            {"id": "pb1", "name": "Employment Playbook", "case_type": "Employment Dispute"}
        ]
        
        mock_file.return_value = mock_open(read_data=json.dumps(playbooks_data)).return_value
        
        result = PlaybookService.match_playbook("Employment Dispute")
        
        assert result is not None
        assert result["id"] == "pb1"

    @patch("builtins.open", new_callable=mock_open)
    @patch("pathlib.Path.exists", return_value=True)
    def test_match_playbook_no_match(self, mock_exists, mock_file):
        """Test playbook matching when no match found"""
        playbooks_data = {
            "playbooks": [
                {"id": "pb1", "case_type": "Employment Dispute"}
            ]
        }
        
        mock_file.return_value = mock_open(read_data=json.dumps(playbooks_data)).return_value
        
        result = PlaybookService.match_playbook("Intellectual Property")
        
        assert result is None

    @patch("pathlib.Path.exists", return_value=False)
    def test_match_playbook_file_not_exists(self, mock_exists):
        """Test playbook matching when file doesn't exist"""
        result = PlaybookService.match_playbook("Employment Dispute")
        
        assert result is None

    @patch("builtins.open", side_effect=Exception("File error"))
    @patch("pathlib.Path.exists", return_value=True)
    def test_match_playbook_exception(self, mock_exists, mock_file):
        """Test playbook matching with exception"""
        result = PlaybookService.match_playbook("Employment Dispute")
        
        assert result is None

    @patch("app.services.data_service.DataService.load_cases")
    @patch.object(PlaybookService, "match_playbook")
    def test_analyze_case_with_playbook_success(self, mock_match, mock_load_cases):
        """Test successful case analysis with playbook"""
        # Mock case data
        mock_case = {
            "id": "case1",
            "case_type": "Employment Dispute",
            "summary": "Employee termination within protected period with age discrimination"
        }
        mock_load_cases.return_value = [mock_case]
        
        # Mock playbook data
        mock_playbook = {
            "id": "pb1",
            "name": "Employment Playbook",
            "case_type": "Employment Dispute",
            "rules": [
                {
                    "id": "rule1",
                    "condition": "termination_within_protected_period",
                    "weight": 0.9,
                    "action": "Investigate protected activity",
                    "description": "Strong case for retaliation",
                    "evidence_required": ["Termination notice", "Protected activity documentation"]
                }
            ]
        }
        mock_match.return_value = mock_playbook
        
        result = PlaybookService.analyze_case_with_playbook("case1")
        
        assert result["case_id"] == "case1"
        assert "case_strength_assessment" in result
        assert "strategic_recommendations" in result
        assert "relevant_precedents" in result
        assert "applied_playbook" in result
        assert result["applied_playbook"]["id"] == "pb1"

    @patch("app.services.data_service.DataService.load_cases")
    def test_analyze_case_with_playbook_case_not_found(self, mock_load_cases):
        """Test case analysis when case not found"""
        mock_load_cases.return_value = []
        
        result = PlaybookService.analyze_case_with_playbook("nonexistent")
        
        assert result["case_id"] == "nonexistent"
        assert result["applied_playbook"] is None
        assert "fallback_reason" in result
        assert "Case not found" in result["fallback_reason"]

    @patch("app.services.data_service.DataService.load_cases")
    def test_analyze_case_with_playbook_no_case_type(self, mock_load_cases):
        """Test case analysis when case has no case_type"""
        mock_case = {"id": "case1", "summary": "Test case"}
        mock_load_cases.return_value = [mock_case]
        
        result = PlaybookService.analyze_case_with_playbook("case1")
        
        assert "No case type specified" in result["fallback_reason"]

    @patch("app.services.data_service.DataService.load_cases")
    @patch.object(PlaybookService, "match_playbook")
    def test_analyze_case_with_playbook_no_playbook_match(self, mock_match, mock_load_cases):
        """Test case analysis when no playbook matches"""
        mock_case = {"id": "case1", "case_type": "Unknown Type"}
        mock_load_cases.return_value = [mock_case]
        mock_match.return_value = None
        
        result = PlaybookService.analyze_case_with_playbook("case1")
        
        assert "No playbook found for case type" in result["fallback_reason"]

    def test_apply_playbook_rules_no_rules(self):
        """Test applying playbook rules when no rules exist"""
        case = {"id": "case1", "summary": "Test case"}
        playbook = {"id": "pb1", "rules": []}
        
        result = PlaybookService._apply_playbook_rules(case, playbook)
        
        assert result["case_strength"] == "Weak"
        assert result["confidence_level"] == 0.2
        assert len(result["applied_rules"]) == 0
        assert "No applicable rules found" in result["potential_weaknesses"]

    def test_apply_playbook_rules_with_matching_rules(self):
        """Test applying playbook rules with matching conditions"""
        case = {
            "id": "case1",
            "summary": "Employee termination within protected period due to age discrimination",
            "case_type": "Employment Dispute"
        }
        playbook = {
            "id": "pb1",
            "rules": [
                {
                    "id": "rule1",
                    "condition": "termination_within_protected_period",
                    "weight": 0.9,
                    "action": "Investigate protected activity",
                    "description": "Strong retaliation case",
                    "evidence_required": ["Termination notice"]
                },
                {
                    "id": "rule2",
                    "condition": "age_over_40_and_replaced_by_younger",
                    "weight": 0.8,
                    "action": "Gather age discrimination evidence",
                    "description": "Age discrimination indicators",
                    "evidence_required": ["Age documentation"]
                }
            ]
        }
        
        result = PlaybookService._apply_playbook_rules(case, playbook)
        
        assert len(result["applied_rules"]) == 2
        assert "rule1" in result["applied_rules"]
        assert "rule2" in result["applied_rules"]
        assert result["case_strength"] in ["Strong", "Moderate"]
        assert result["confidence_level"] > 0.5

    def test_apply_playbook_rules_with_non_matching_rules(self):
        """Test applying playbook rules with non-matching conditions"""
        case = {
            "id": "case1",
            "summary": "Simple contract dispute",
            "case_type": "Contract"
        }
        playbook = {
            "id": "pb1",
            "rules": [
                {
                    "id": "rule1",
                    "condition": "termination_within_protected_period",
                    "weight": 0.9,
                    "action": "Investigate",
                    "description": "Important rule"
                }
            ]
        }
        
        result = PlaybookService._apply_playbook_rules(case, playbook)
        
        assert len(result["applied_rules"]) == 0
        assert result["case_strength"] == "Weak"
        assert len(result["potential_weaknesses"]) > 0

    def test_evaluate_rule_condition_keyword_matching(self):
        """Test rule condition evaluation with keyword matching"""
        case = {
            "summary": "Employee was terminated and fired from the company",
            "case_type": "Employment"
        }
        rule = {"condition": "termination_within_protected_period"}
        
        result = PlaybookService._evaluate_rule_condition(case, rule)
        
        assert result is True

    def test_evaluate_rule_condition_no_match(self):
        """Test rule condition evaluation with no keyword match"""
        case = {
            "summary": "Simple contract negotiation",
            "case_type": "Contract"
        }
        rule = {"condition": "termination_within_protected_period"}
        
        result = PlaybookService._evaluate_rule_condition(case, rule)
        
        assert result is False

    def test_evaluate_rule_condition_fallback_matching(self):
        """Test rule condition evaluation with fallback substring matching"""
        case = {
            "summary": "Custom condition test case",
            "case_type": "Test"
        }
        rule = {"condition": "custom condition"}
        
        result = PlaybookService._evaluate_rule_condition(case, rule)
        
        assert result is True

    def test_calculate_case_strength_and_confidence_no_rules(self):
        """Test case strength calculation with no applied rules"""
        strength, confidence = PlaybookService._calculate_case_strength_and_confidence(0.0, 0, 5)
        
        assert strength == "Weak"
        assert confidence == 0.2

    def test_calculate_case_strength_and_confidence_strong_case(self):
        """Test case strength calculation for strong case"""
        # High weight, good coverage
        strength, confidence = PlaybookService._calculate_case_strength_and_confidence(4.0, 4, 5)
        
        assert strength == "Strong"
        assert confidence >= 0.7

    def test_calculate_case_strength_and_confidence_moderate_case(self):
        """Test case strength calculation for moderate case"""
        # Medium weight, medium coverage
        strength, confidence = PlaybookService._calculate_case_strength_and_confidence(2.4, 3, 5)
        
        assert strength == "Moderate"
        assert confidence >= 0.5

    def test_calculate_case_strength_and_confidence_weak_case(self):
        """Test case strength calculation for weak case"""
        # Low weight, low coverage
        strength, confidence = PlaybookService._calculate_case_strength_and_confidence(1.0, 1, 5)
        
        assert strength == "Weak"
        assert confidence <= 0.5

    def test_generate_reasoning_no_rules(self):
        """Test reasoning generation with no applied rules"""
        reasoning = PlaybookService._generate_reasoning([], "Weak", 5)
        
        assert "No applicable rules found" in reasoning
        assert "inconclusive" in reasoning

    def test_generate_reasoning_with_rules(self):
        """Test reasoning generation with applied rules"""
        applied_rules = ["rule1", "rule2", "rule3"]
        reasoning = PlaybookService._generate_reasoning(applied_rules, "Strong", 5)
        
        assert "3 applicable rules" in reasoning
        assert "out of 5 total rules" in reasoning
        assert "strong prospects" in reasoning

    def test_generate_strategic_recommendations_strong_case(self):
        """Test strategic recommendations for strong case"""
        playbook_result = {
            "case_strength": "Strong",
            "applied_rules": ["rule1"]
        }
        
        recommendations = PlaybookService._generate_strategic_recommendations(playbook_result)
        
        assert len(recommendations) > 0
        assert any("Full Compensatory Damages" in rec["title"] for rec in recommendations)
        assert any(rec["priority"] == "High" for rec in recommendations)

    def test_generate_strategic_recommendations_moderate_case(self):
        """Test strategic recommendations for moderate case"""
        playbook_result = {
            "case_strength": "Moderate",
            "applied_rules": ["rule1"]
        }
        
        recommendations = PlaybookService._generate_strategic_recommendations(playbook_result)
        
        assert len(recommendations) > 0
        assert any("Settlement" in rec["title"] for rec in recommendations)

    def test_generate_strategic_recommendations_weak_case(self):
        """Test strategic recommendations for weak case"""
        playbook_result = {
            "case_strength": "Weak",
            "applied_rules": []
        }
        
        recommendations = PlaybookService._generate_strategic_recommendations(playbook_result)
        
        assert len(recommendations) > 0
        assert any("Settlement" in rec["title"] or "Risks" in rec["title"] for rec in recommendations)

    def test_generate_strategic_recommendations_rule_specific(self):
        """Test rule-specific strategic recommendations"""
        playbook_result = {
            "case_strength": "Moderate",
            "applied_rules": ["termination_rule", "breach_rule"]
        }
        
        recommendations = PlaybookService._generate_strategic_recommendations(playbook_result)
        
        # Should include rule-specific recommendations
        assert any("Termination" in rec["title"] for rec in recommendations)
        assert any("Contract" in rec["title"] for rec in recommendations)
        # Should limit to 5 recommendations
        assert len(recommendations) <= 5

    def test_get_relevant_precedents_employment(self):
        """Test getting relevant precedents for employment cases"""
        precedents = PlaybookService._get_relevant_precedents("Employment Dispute")
        
        assert len(precedents) > 0
        assert any("Employment Rights Act" in prec["title"] for prec in precedents)
        assert any("Equality Act" in prec["title"] for prec in precedents)

    def test_get_relevant_precedents_contract(self):
        """Test getting relevant precedents for contract cases"""
        precedents = PlaybookService._get_relevant_precedents("Contract Breach")
        
        assert len(precedents) > 0
        assert any("Sale of Goods Act" in prec["title"] for prec in precedents)
        assert any("Unfair Contract Terms" in prec["title"] for prec in precedents)

    def test_get_relevant_precedents_ip(self):
        """Test getting relevant precedents for IP cases"""
        precedents = PlaybookService._get_relevant_precedents("Intellectual Property")
        
        assert len(precedents) > 0
        assert any("Copyright" in prec["title"] for prec in precedents)

    def test_get_relevant_precedents_unknown_type(self):
        """Test getting relevant precedents for unknown case type"""
        precedents = PlaybookService._get_relevant_precedents("Unknown Type")
        
        assert precedents == []

    def test_generate_fallback_analysis(self):
        """Test fallback analysis generation"""
        case_id = "test_case"
        reason = "Test reason"
        
        result = PlaybookService._generate_fallback_analysis(case_id, reason)
        
        assert result["case_id"] == case_id
        assert result["fallback_reason"] == reason
        assert result["applied_playbook"] is None
        assert result["case_strength_assessment"]["overall_strength"] == "Unknown"
        assert result["case_strength_assessment"]["confidence_level"] == 0.1
        assert len(result["strategic_recommendations"]) > 0
        assert "analysis_timestamp" in result

    @patch("app.services.data_service.DataService.load_cases")
    def test_analyze_case_with_playbook_exception_handling(self, mock_load_cases):
        """Test exception handling in case analysis"""
        mock_load_cases.side_effect = Exception("Database error")
        
        result = PlaybookService.analyze_case_with_playbook("case1")
        
        assert result["case_id"] == "case1"
        assert "fallback_reason" in result
        assert "Analysis error" in result["fallback_reason"]

    def test_comprehensive_rule_evaluation_scenarios(self):
        """Test comprehensive rule evaluation scenarios"""
        test_cases = [
            {
                "condition": "termination_within_protected_period",
                "case_summary": "employee was terminated and fired after filing complaint",
                "expected": True
            },
            {
                "condition": "age_over_40_and_replaced_by_younger",
                "case_summary": "age discrimination with younger replacement",
                "expected": True
            },
            {
                "condition": "clear_contract_terms_violated",
                "case_summary": "breach of contract with violation of terms",
                "expected": True
            },
            {
                "condition": "debtor_has_assets",
                "case_summary": "debtor owns property and has income",
                "expected": True
            },
            {
                "condition": "nonexistent_condition",
                "case_summary": "random case summary",
                "expected": False
            }
        ]
        
        for test_case in test_cases:
            case = {
                "summary": test_case["case_summary"],
                "case_type": "Test"
            }
            rule = {"condition": test_case["condition"]}
            
            result = PlaybookService._evaluate_rule_condition(case, rule)
            assert result == test_case["expected"], f"Failed for condition: {test_case['condition']}"

    def test_integration_full_analysis_workflow(self):
        """Integration test for full analysis workflow"""
        with patch("app.services.data_service.DataService.load_cases") as mock_load_cases:
            with patch.object(PlaybookService, "match_playbook") as mock_match:
                # Setup comprehensive test data
                mock_case = {
                    "id": "integration_case",
                    "case_type": "Employment Dispute",
                    "summary": "Employee termination within protected period with age discrimination and documented performance issues"
                }
                mock_load_cases.return_value = [mock_case]
                
                mock_playbook = {
                    "id": "employment_pb",
                    "name": "Employment Dispute Playbook",
                    "case_type": "Employment Dispute",
                    "rules": [
                        {
                            "id": "protected_termination",
                            "condition": "termination_within_protected_period",
                            "weight": 0.9,
                            "action": "Investigate retaliation",
                            "description": "Strong retaliation case",
                            "evidence_required": ["Protected activity proof", "Termination timeline"]
                        },
                        {
                            "id": "age_discrimination",
                            "condition": "age_over_40_and_replaced_by_younger",
                            "weight": 0.8,
                            "action": "Gather age evidence",
                            "description": "Age discrimination indicators",
                            "evidence_required": ["Age documentation", "Replacement evidence"]
                        },
                        {
                            "id": "performance_issues",
                            "condition": "documented_performance_issues",
                            "weight": 0.6,
                            "action": "Review performance records",
                            "description": "Performance documentation exists",
                            "evidence_required": ["Performance reviews"]
                        }
                    ]
                }
                mock_match.return_value = mock_playbook
                
                result = PlaybookService.analyze_case_with_playbook("integration_case")
                
                # Verify comprehensive analysis
                assert result["case_id"] == "integration_case"
                assert result["applied_playbook"]["id"] == "employment_pb"
                
                # Should have applied multiple rules
                strength_assessment = result["case_strength_assessment"]
                assert strength_assessment["overall_strength"] in ["Strong", "Moderate"]
                assert strength_assessment["confidence_level"] > 0.5
                assert len(strength_assessment["key_strengths"]) > 0
                assert len(strength_assessment["supporting_evidence"]) > 0
                
                # Should have strategic recommendations
                assert len(result["strategic_recommendations"]) > 0
                assert all("id" in rec for rec in result["strategic_recommendations"])
                assert all("priority" in rec for rec in result["strategic_recommendations"])
                
                # Should have relevant precedents
                assert len(result["relevant_precedents"]) > 0