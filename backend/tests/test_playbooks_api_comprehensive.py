#!/usr/bin/env python3
"""
Comprehensive test suite for Playbooks API endpoints

This module provides complete test coverage for all playbook-related API endpoints including:
- Playbook listing and retrieval
- Case type matching
- Comprehensive case analysis using playbooks
- Playbook rule application and evaluation
"""

import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from main import app

client = TestClient(app)


class TestPlaybookListing:
    """Test playbook listing functionality"""
    
    def test_get_all_playbooks_success(self):
        """Test successful retrieval of all playbooks"""
        with patch('app.services.data_service.DataService.load_playbooks') as mock_load:
            mock_load.return_value = [
                {
                    "id": "employment-dispute",
                    "case_type": "Employment Dispute",
                    "name": "Employment Law Playbook",
                    "rules": [
                        {
                            "id": "rule-001",
                            "condition": "termination_within_protected_period",
                            "action": "investigate_victimisation_claim",
                            "weight": 0.9,
                            "description": "If dismissal occurred within 90 days of protected activity"
                        }
                    ],
                    "decision_tree": {
                        "root": "assess_termination_circumstances",
                        "nodes": {
                            "assess_termination_circumstances": {
                                "question": "Was termination within 90 days of protected activity?",
                                "yes": "high_strength",
                                "no": "assess_other_factors"
                            }
                        }
                    },
                    "monetary_ranges": {
                        "high": {"range": [200000, 1000000], "description": "Strong case with clear evidence"},
                        "moderate": {"range": [50000, 200000], "description": "Reasonable prospects"},
                        "low": {"range": [5000, 50000], "description": "Limited prospects"}
                    },
                    "escalation_paths": [
                        "Internal HR complaint",
                        "ACAS early conciliation",
                        "Employment tribunal claim"
                    ]
                },
                {
                    "id": "contract-dispute",
                    "case_type": "Contract Dispute",
                    "name": "Contract Law Playbook",
                    "rules": [
                        {
                            "id": "rule-101",
                            "condition": "breach_of_material_term",
                            "action": "assess_damages",
                            "weight": 0.8,
                            "description": "Material breach of contract terms"
                        }
                    ],
                    "decision_tree": {},
                    "monetary_ranges": {},
                    "escalation_paths": []
                }
            ]
            
            response = client.get("/playbooks/")
            
            assert response.status_code == 200
            data = response.json()
            assert len(data) == 2
            assert data[0]["id"] == "employment-dispute"
            assert data[0]["case_type"] == "Employment Dispute"
            assert len(data[0]["rules"]) == 1
            assert data[0]["rules"][0]["weight"] == 0.9
            assert data[1]["id"] == "contract-dispute"
            mock_load.assert_called_once()
    
    def test_get_all_playbooks_empty(self):
        """Test playbook listing with no playbooks available"""
        with patch('app.services.data_service.DataService.load_playbooks') as mock_load:
            mock_load.return_value = []
            
            response = client.get("/playbooks/")
            
            assert response.status_code == 200
            data = response.json()
            assert len(data) == 0
    
    def test_get_all_playbooks_service_error(self):
        """Test playbook listing handles service errors"""
        with patch('app.services.data_service.DataService.load_playbooks') as mock_load:
            mock_load.side_effect = Exception("Database connection failed")
            
            response = client.get("/playbooks/")
            
            assert response.status_code == 500
            assert "Failed to get playbooks" in response.json()["detail"]


class TestPlaybookRetrieval:
    """Test individual playbook retrieval by case type"""
    
    def test_get_playbook_success(self):
        """Test successful retrieval of playbook by case type"""
        with patch('app.services.playbook_service.PlaybookService.match_playbook') as mock_match:
            mock_match.return_value = {
                "id": "employment-dispute",
                "case_type": "Employment Dispute",
                "name": "Employment Law Playbook",
                "rules": [
                    {
                        "id": "rule-001",
                        "condition": "termination_within_protected_period",
                        "action": "investigate_victimisation_claim",
                        "weight": 0.9,
                        "description": "If dismissal occurred within 90 days of protected activity, investigate potential victimisation",
                        "legal_basis": "Employment Rights Act 1996, s.103A",
                        "evidence_required": ["Timeline of protected activity", "Dismissal documentation"]
                    },
                    {
                        "id": "rule-002",
                        "condition": "lack_of_fair_procedure",
                        "action": "assess_procedural_unfairness",
                        "weight": 0.7,
                        "description": "Assess whether proper dismissal procedures were followed",
                        "legal_basis": "ACAS Code of Practice",
                        "evidence_required": ["HR documentation", "Meeting records"]
                    }
                ],
                "decision_tree": {
                    "root": "assess_termination_circumstances",
                    "nodes": {
                        "assess_termination_circumstances": {
                            "question": "Was termination within 90 days of protected activity?",
                            "yes": "high_strength",
                            "no": "assess_other_factors"
                        },
                        "assess_other_factors": {
                            "question": "Were proper procedures followed?",
                            "yes": "low_strength",
                            "no": "moderate_strength"
                        }
                    }
                },
                "monetary_ranges": {
                    "high": {
                        "range": [200000, 1000000],
                        "description": "Strong case with clear evidence of victimisation"
                    },
                    "moderate": {
                        "range": [50000, 200000],
                        "description": "Reasonable prospects with some supporting evidence"
                    },
                    "low": {
                        "range": [5000, 50000],
                        "description": "Limited prospects, procedural issues only"
                    }
                },
                "escalation_paths": [
                    "Internal HR complaint",
                    "ACAS early conciliation",
                    "Employment tribunal claim",
                    "Appeal to Employment Appeal Tribunal"
                ]
            }
            
            response = client.get("/playbooks/Employment Dispute")
            
            assert response.status_code == 200
            data = response.json()
            assert data["id"] == "employment-dispute"
            assert data["case_type"] == "Employment Dispute"
            assert len(data["rules"]) == 2
            assert data["rules"][0]["weight"] == 0.9
            assert "legal_basis" in data["rules"][0]
            assert "evidence_required" in data["rules"][0]
            assert "decision_tree" in data
            assert "monetary_ranges" in data
            assert len(data["escalation_paths"]) == 4
            mock_match.assert_called_once_with("Employment Dispute")
    
    def test_get_playbook_not_found(self):
        """Test playbook retrieval with non-existent case type"""
        with patch('app.services.playbook_service.PlaybookService.match_playbook') as mock_match:
            mock_match.return_value = None
            
            response = client.get("/playbooks/Unknown Type")
            
            assert response.status_code == 404
            assert "No playbook found for case type: Unknown Type" in response.json()["detail"]
    
    def test_get_playbook_service_error(self):
        """Test playbook retrieval handles service errors"""
        with patch('app.services.playbook_service.PlaybookService.match_playbook') as mock_match:
            mock_match.side_effect = Exception("Playbook service unavailable")
            
            response = client.get("/playbooks/Employment Dispute")
            
            assert response.status_code == 500
            assert "Failed to get playbook" in response.json()["detail"]


class TestPlaybookMatching:
    """Test playbook matching functionality"""
    
    def test_match_playbook_success(self):
        """Test successful playbook matching"""
        with patch('app.services.playbook_service.PlaybookService.match_playbook') as mock_match:
            mock_match.return_value = {
                "id": "employment-dispute",
                "case_type": "Employment Dispute",
                "name": "Employment Law Playbook",
                "description": "Comprehensive playbook for employment-related legal disputes"
            }
            
            response = client.get("/playbooks/match/Employment Dispute")
            
            assert response.status_code == 200
            data = response.json()
            assert data["id"] == "employment-dispute"
            assert data["case_type"] == "Employment Dispute"
            assert data["name"] == "Employment Law Playbook"
            assert "description" in data
            mock_match.assert_called_once_with("Employment Dispute")
    
    def test_match_playbook_not_found(self):
        """Test playbook matching with no matching playbook"""
        with patch('app.services.playbook_service.PlaybookService.match_playbook') as mock_match:
            mock_match.return_value = None
            
            response = client.get("/playbooks/match/Unsupported Type")
            
            assert response.status_code == 404
            assert "No playbook found for case type: Unsupported Type" in response.json()["detail"]
    
    def test_match_playbook_service_error(self):
        """Test playbook matching handles service errors"""
        with patch('app.services.playbook_service.PlaybookService.match_playbook') as mock_match:
            mock_match.side_effect = Exception("Matching service failed")
            
            response = client.get("/playbooks/match/Employment Dispute")
            
            assert response.status_code == 500
            assert "Failed to match playbook" in response.json()["detail"]


class TestComprehensiveAnalysis:
    """Test comprehensive case analysis using playbooks"""
    
    def test_generate_comprehensive_analysis_success(self):
        """Test successful comprehensive case analysis"""
        with patch('app.services.playbook_service.PlaybookService.analyze_case_with_playbook') as mock_analyze:
            mock_analyze.return_value = {
                "case_id": "case-001",
                "case_strength_assessment": {
                    "overall_strength": "Moderate",
                    "confidence_level": 0.75,
                    "key_strengths": [
                        "Strong legal position on victimisation claim",
                        "Clear timeline of protected activity",
                        "Documented evidence of retaliation"
                    ],
                    "potential_weaknesses": [
                        "Limited witness testimony",
                        "Some procedural compliance by employer"
                    ],
                    "supporting_evidence": [
                        "Timeline of protected activity and subsequent dismissal",
                        "Email communications showing management awareness",
                        "Performance reviews prior to protected activity"
                    ]
                },
                "strategic_recommendations": [
                    {
                        "id": "negotiate_settlement",
                        "title": "Negotiate Favorable Settlement",
                        "description": "Given moderate case strength, pursue settlement negotiations before tribunal",
                        "priority": "High",
                        "rationale": "Moderate case strength with 75% confidence suggests settlement may be optimal strategy",
                        "supporting_precedents": [
                            "Risk mitigation for both parties",
                            "Cost-effective resolution",
                            "Confidentiality benefits"
                        ],
                        "estimated_timeline": "2-4 weeks",
                        "success_probability": 0.7
                    },
                    {
                        "id": "strengthen_evidence",
                        "title": "Strengthen Evidence Base",
                        "description": "Gather additional witness statements and documentation",
                        "priority": "Medium",
                        "rationale": "Additional evidence could improve case strength significantly",
                        "supporting_precedents": [
                            "Witness testimony importance in employment cases",
                            "Documentary evidence standards"
                        ],
                        "estimated_timeline": "3-6 weeks",
                        "success_probability": 0.6
                    }
                ],
                "relevant_precedents": [
                    {
                        "id": "employment_precedent_1",
                        "title": "Employment Rights Act 1996 - Unfair Dismissal",
                        "category": "statutes",
                        "relevance": "Primary legislation governing employment termination and protected disclosures",
                        "key_points": [
                            "Protected disclosure provisions",
                            "Automatic unfair dismissal categories",
                            "Remedies and compensation"
                        ]
                    },
                    {
                        "id": "employment_precedent_2",
                        "title": "Cavendish Munro Professional Risks Management Ltd v Geduld",
                        "category": "case_law",
                        "relevance": "Leading case on victimisation and protected disclosures",
                        "key_points": [
                            "Causation requirements for victimisation claims",
                            "Burden of proof considerations",
                            "Remedies available"
                        ]
                    }
                ],
                "applied_playbook": {
                    "id": "employment-dispute",
                    "name": "Employment Law Playbook",
                    "case_type": "Employment Dispute",
                    "rules_applied": [
                        {
                            "rule_id": "rule-001",
                            "condition": "termination_within_protected_period",
                            "result": "matched",
                            "confidence": 0.9,
                            "contribution_to_strength": 0.4
                        },
                        {
                            "rule_id": "rule-002",
                            "condition": "lack_of_fair_procedure",
                            "result": "partial_match",
                            "confidence": 0.6,
                            "contribution_to_strength": 0.2
                        }
                    ]
                },
                "analysis_timestamp": "2024-01-15T10:30:00Z",
                "analysis_version": "1.0",
                "confidence_factors": {
                    "evidence_quality": 0.8,
                    "legal_precedent_strength": 0.7,
                    "procedural_compliance": 0.6,
                    "witness_availability": 0.5
                }
            }
            
            response = client.post("/playbooks/cases/case-001/comprehensive-analysis")
            
            assert response.status_code == 200
            data = response.json()
            assert data["case_id"] == "case-001"
            assert data["case_strength_assessment"]["overall_strength"] == "Moderate"
            assert data["case_strength_assessment"]["confidence_level"] == 0.75
            assert len(data["case_strength_assessment"]["key_strengths"]) == 3
            assert len(data["strategic_recommendations"]) == 2
            assert data["strategic_recommendations"][0]["priority"] == "High"
            assert len(data["relevant_precedents"]) == 2
            assert data["applied_playbook"]["id"] == "employment-dispute"
            assert len(data["applied_playbook"]["rules_applied"]) == 2
            assert "confidence_factors" in data
            mock_analyze.assert_called_once_with("case-001")
    
    def test_generate_comprehensive_analysis_case_not_found(self):
        """Test comprehensive analysis with non-existent case"""
        with patch('app.services.playbook_service.PlaybookService.analyze_case_with_playbook') as mock_analyze:
            mock_analyze.side_effect = Exception("Case with ID case-999 not found")
            
            response = client.post("/playbooks/cases/case-999/comprehensive-analysis")
            
            assert response.status_code == 500
            assert "Failed to perform comprehensive analysis" in response.json()["detail"]
    
    def test_generate_comprehensive_analysis_no_playbook(self):
        """Test comprehensive analysis when no matching playbook exists"""
        with patch('app.services.playbook_service.PlaybookService.analyze_case_with_playbook') as mock_analyze:
            mock_analyze.side_effect = Exception("No playbook found for case type")
            
            response = client.post("/playbooks/cases/case-001/comprehensive-analysis")
            
            assert response.status_code == 500
            assert "Failed to perform comprehensive analysis" in response.json()["detail"]
    
    def test_generate_comprehensive_analysis_service_error(self):
        """Test comprehensive analysis handles service errors"""
        with patch('app.services.playbook_service.PlaybookService.analyze_case_with_playbook') as mock_analyze:
            mock_analyze.side_effect = Exception("Analysis service temporarily unavailable")
            
            response = client.post("/playbooks/cases/case-001/comprehensive-analysis")
            
            assert response.status_code == 500
            assert "Failed to perform comprehensive analysis" in response.json()["detail"]


class TestPlaybookIntegration:
    """Integration tests for playbook API endpoints"""
    
    def test_playbook_workflow_integration(self):
        """Test complete playbook workflow from listing to analysis"""
        # Mock all required services
        with patch('app.services.data_service.DataService.load_playbooks') as mock_load, \
             patch('app.services.playbook_service.PlaybookService.match_playbook') as mock_match, \
             patch('app.services.playbook_service.PlaybookService.analyze_case_with_playbook') as mock_analyze:
            
            # Setup mock data
            mock_load.return_value = [
                {
                    "id": "employment-dispute",
                    "case_type": "Employment Dispute",
                    "name": "Employment Law Playbook",
                    "rules": []
                }
            ]
            
            mock_match.return_value = {
                "id": "employment-dispute",
                "case_type": "Employment Dispute",
                "name": "Employment Law Playbook",
                "rules": [
                    {
                        "id": "rule-001",
                        "condition": "termination_within_protected_period",
                        "weight": 0.9
                    }
                ]
            }
            
            mock_analyze.return_value = {
                "case_id": "case-001",
                "case_strength_assessment": {
                    "overall_strength": "High",
                    "confidence_level": 0.85
                },
                "strategic_recommendations": [],
                "relevant_precedents": [],
                "applied_playbook": {
                    "id": "employment-dispute",
                    "name": "Employment Law Playbook"
                },
                "analysis_timestamp": "2024-01-15T10:30:00Z"
            }
            
            # Test workflow: List -> Match -> Get -> Analyze
            
            # 1. List all playbooks
            list_response = client.get("/playbooks/")
            assert list_response.status_code == 200
            playbooks = list_response.json()
            assert len(playbooks) == 1
            
            # 2. Match playbook for case type
            case_type = playbooks[0]["case_type"]
            match_response = client.get(f"/playbooks/match/{case_type}")
            assert match_response.status_code == 200
            match_data = match_response.json()
            assert match_data["id"] == "employment-dispute"
            
            # 3. Get full playbook details
            playbook_response = client.get(f"/playbooks/{case_type}")
            assert playbook_response.status_code == 200
            playbook_data = playbook_response.json()
            assert len(playbook_data["rules"]) == 1
            
            # 4. Perform comprehensive analysis
            analysis_response = client.post("/playbooks/cases/case-001/comprehensive-analysis")
            assert analysis_response.status_code == 200
            analysis_data = analysis_response.json()
            assert analysis_data["case_strength_assessment"]["overall_strength"] == "High"
    
    def test_playbook_error_handling_integration(self):
        """Test playbook API error handling across endpoints"""
        # Test cascading error handling when playbook service is down
        with patch('app.services.data_service.DataService.load_playbooks') as mock_load, \
             patch('app.services.playbook_service.PlaybookService.match_playbook') as mock_match:
            
            mock_load.side_effect = Exception("Service unavailable")
            mock_match.side_effect = Exception("Service unavailable")
            
            # All endpoints should handle service errors gracefully
            list_response = client.get("/playbooks/")
            assert list_response.status_code == 500
            
            match_response = client.get("/playbooks/match/Employment Dispute")
            assert match_response.status_code == 500
            
            get_response = client.get("/playbooks/Employment Dispute")
            assert get_response.status_code == 500
    
    def test_playbook_case_type_variations(self):
        """Test playbook endpoints handle various case type formats"""
        with patch('app.services.playbook_service.PlaybookService.match_playbook') as mock_match:
            mock_match.return_value = {
                "id": "employment-dispute",
                "case_type": "Employment Dispute",
                "name": "Employment Law Playbook"
            }
            
            # Test different case type formats
            test_cases = [
                "Employment Dispute",
                "employment-dispute",
                "EMPLOYMENT DISPUTE",
                "Employment%20Dispute"  # URL encoded
            ]
            
            for case_type in test_cases:
                response = client.get(f"/playbooks/match/{case_type}")
                assert response.status_code == 200
                data = response.json()
                assert data["id"] == "employment-dispute"


if __name__ == "__main__":
    pytest.main([__file__])