#!/usr/bin/env python3
"""
API Tests for AI Analysis Endpoints

Tests for the AI analysis endpoints in the cases API including:
- POST /api/cases/{case_id}/ai-analysis
- GET /api/cases/{case_id}/ai-analysis  
- GET /api/cases/{case_id}/ai-conversations
"""

import pytest
import json
import os
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient
from pathlib import Path


class TestAIAnalysisEndpoints:
    """Test class for AI analysis API endpoints"""
    
    def test_trigger_ai_analysis_success(self, client, sample_case_data):
        """Test successful AI analysis trigger"""
        case_id = "case-001"
        
        # Mock the services
        with patch('app.api.cases.CasesService.load_cases') as mock_load_cases, \
             patch('app.api.cases.AIAnalysisService') as mock_ai_service:
            
            # Setup mocks
            mock_load_cases.return_value = [{"id": case_id, **sample_case_data}]
            mock_ai_instance = MagicMock()
            mock_ai_service.return_value = mock_ai_instance
            
            expected_analysis = {
                "case_id": case_id,
                "timestamp": "2024-01-15T10:00:00Z",
                "claim_reference": "CLM-2024-001",
                "claimant_name": "John Smith",
                "incident_date": "2024-01-10",
                "claim_amount": 50000,
                "key_facts": ["Employment terminated", "Age discrimination alleged"],
                "confidence": 0.85
            }
            mock_ai_instance.analyze_case.return_value = expected_analysis
            
            # Make request
            response = client.post(f"/api/cases/{case_id}/ai-analysis")
            
            # Assertions
            assert response.status_code == 200
            data = response.json()
            assert data["success"] is True
            assert data["case_id"] == case_id
            assert data["analysis"] == expected_analysis
            assert "AI analysis completed successfully" in data["message"]
            
            # Verify service calls
            mock_load_cases.assert_called_once()
            mock_ai_instance.analyze_case.assert_called_once_with(case_id)
    
    def test_trigger_ai_analysis_case_not_found(self, client):
        """Test AI analysis trigger with non-existent case"""
        case_id = "non-existent-case"
        
        with patch('app.api.cases.CasesService.load_cases') as mock_load_cases:
            mock_load_cases.return_value = []
            
            response = client.post(f"/api/cases/{case_id}/ai-analysis")
            
            assert response.status_code == 404
            data = response.json()
            assert f"Case {case_id} not found" in data["detail"]
    
    def test_trigger_ai_analysis_validation_error(self, client, sample_case_data):
        """Test AI analysis trigger with validation error"""
        case_id = "case-001"
        
        with patch('app.api.cases.CasesService.load_cases') as mock_load_cases, \
             patch('app.api.cases.AIAnalysisService') as mock_ai_service:
            
            mock_load_cases.return_value = [{"id": case_id, **sample_case_data}]
            mock_ai_instance = MagicMock()
            mock_ai_service.return_value = mock_ai_instance
            mock_ai_instance.analyze_case.side_effect = ValueError("Invalid document format")
            
            response = client.post(f"/api/cases/{case_id}/ai-analysis")
            
            assert response.status_code == 422
            data = response.json()
            assert "Analysis validation error" in data["detail"]
            assert "Invalid document format" in data["detail"]
    
    def test_trigger_ai_analysis_internal_error(self, client, sample_case_data):
        """Test AI analysis trigger with internal server error"""
        case_id = "case-001"
        
        with patch('app.api.cases.CasesService.load_cases') as mock_load_cases, \
             patch('app.api.cases.AIAnalysisService') as mock_ai_service:
            
            mock_load_cases.return_value = [{"id": case_id, **sample_case_data}]
            mock_ai_instance = MagicMock()
            mock_ai_service.return_value = mock_ai_instance
            mock_ai_instance.analyze_case.side_effect = Exception("Claude API unavailable")
            
            response = client.post(f"/api/cases/{case_id}/ai-analysis")
            
            assert response.status_code == 500
            data = response.json()
            assert "Failed to perform AI analysis" in data["detail"]
    
    def test_get_ai_analysis_success(self, client, sample_case_data):
        """Test successful retrieval of AI analysis results"""
        case_id = "case-001"
        
        with patch('app.api.cases.CasesService.load_cases') as mock_load_cases, \
             patch('app.api.cases.AIAnalysisService') as mock_ai_service:
            
            mock_load_cases.return_value = [{"id": case_id, **sample_case_data}]
            mock_ai_instance = MagicMock()
            mock_ai_service.return_value = mock_ai_instance
            
            expected_analysis = {
                "case_id": case_id,
                "timestamp": "2024-01-15T10:00:00Z",
                "claim_reference": "CLM-2024-001",
                "claimant_name": "John Smith",
                "key_facts": ["Employment terminated", "Age discrimination alleged"],
                "confidence": 0.85
            }
            mock_ai_instance.get_case_analysis.return_value = expected_analysis
            
            response = client.get(f"/api/cases/{case_id}/ai-analysis")
            
            assert response.status_code == 200
            data = response.json()
            assert data["success"] is True
            assert data["case_id"] == case_id
            assert data["analysis"] == expected_analysis
            
            mock_ai_instance.get_case_analysis.assert_called_once_with(case_id)
    
    def test_get_ai_analysis_case_not_found(self, client):
        """Test get AI analysis with non-existent case"""
        case_id = "non-existent-case"
        
        with patch('app.api.cases.CasesService.load_cases') as mock_load_cases:
            mock_load_cases.return_value = []
            
            response = client.get(f"/api/cases/{case_id}/ai-analysis")
            
            assert response.status_code == 404
            data = response.json()
            assert f"Case {case_id} not found" in data["detail"]
    
    def test_get_ai_analysis_not_found(self, client, sample_case_data):
        """Test get AI analysis when no analysis exists"""
        case_id = "case-001"
        
        with patch('app.api.cases.CasesService.load_cases') as mock_load_cases, \
             patch('app.api.cases.AIAnalysisService') as mock_ai_service:
            
            mock_load_cases.return_value = [{"id": case_id, **sample_case_data}]
            mock_ai_instance = MagicMock()
            mock_ai_service.return_value = mock_ai_instance
            mock_ai_instance.get_case_analysis.return_value = None
            
            response = client.get(f"/api/cases/{case_id}/ai-analysis")
            
            assert response.status_code == 404
            data = response.json()
            assert f"No AI analysis found for case {case_id}" in data["detail"]
    
    def test_get_ai_conversations_success(self, client, sample_case_data):
        """Test successful retrieval of AI conversation log"""
        case_id = "case-001"
        
        with patch('app.api.cases.CasesService.load_cases') as mock_load_cases, \
             patch('app.api.cases.AIAnalysisService') as mock_ai_service:
            
            mock_load_cases.return_value = [{"id": case_id, **sample_case_data}]
            mock_ai_instance = MagicMock()
            mock_ai_service.return_value = mock_ai_instance
            
            expected_conversations = [
                {
                    "id": "conv-001",
                    "timestamp": "2024-01-15T10:00:00Z",
                    "analysis_type": "case_analysis",
                    "prompt": "Analyze the following case documents...",
                    "response": "Based on the documents, I found...",
                    "metadata": {
                        "documents_analyzed": ["doc-001", "doc-002"],
                        "processing_time": 45.2,
                        "api_version": "claude-3"
                    }
                },
                {
                    "id": "conv-002", 
                    "timestamp": "2024-01-15T11:00:00Z",
                    "analysis_type": "document_review",
                    "prompt": "Review this employment contract...",
                    "response": "The contract contains...",
                    "metadata": {
                        "documents_analyzed": ["doc-003"],
                        "processing_time": 23.1,
                        "api_version": "claude-3"
                    }
                }
            ]
            mock_ai_instance.get_conversation_log.return_value = expected_conversations
            
            response = client.get(f"/api/cases/{case_id}/ai-conversations")
            
            assert response.status_code == 200
            data = response.json()
            assert data["success"] is True
            assert data["case_id"] == case_id
            assert data["conversations"] == expected_conversations
            assert data["total_conversations"] == 2
            
            mock_ai_instance.get_conversation_log.assert_called_once_with(case_id)
    
    def test_get_ai_conversations_empty_log(self, client, sample_case_data):
        """Test get AI conversations with empty conversation log"""
        case_id = "case-001"
        
        with patch('app.api.cases.CasesService.load_cases') as mock_load_cases, \
             patch('app.api.cases.AIAnalysisService') as mock_ai_service:
            
            mock_load_cases.return_value = [{"id": case_id, **sample_case_data}]
            mock_ai_instance = MagicMock()
            mock_ai_service.return_value = mock_ai_instance
            mock_ai_instance.get_conversation_log.return_value = []
            
            response = client.get(f"/api/cases/{case_id}/ai-conversations")
            
            assert response.status_code == 200
            data = response.json()
            assert data["success"] is True
            assert data["case_id"] == case_id
            assert data["conversations"] == []
            assert data["total_conversations"] == 0
    
    def test_get_ai_conversations_case_not_found(self, client):
        """Test get AI conversations with non-existent case"""
        case_id = "non-existent-case"
        
        with patch('app.api.cases.CasesService.load_cases') as mock_load_cases:
            mock_load_cases.return_value = []
            
            response = client.get(f"/api/cases/{case_id}/ai-conversations")
            
            assert response.status_code == 404
            data = response.json()
            assert f"Case {case_id} not found" in data["detail"]
    
    def test_get_ai_conversations_internal_error(self, client, sample_case_data):
        """Test get AI conversations with internal server error"""
        case_id = "case-001"
        
        with patch('app.api.cases.CasesService.load_cases') as mock_load_cases, \
             patch('app.api.cases.AIAnalysisService') as mock_ai_service:
            
            mock_load_cases.return_value = [{"id": case_id, **sample_case_data}]
            mock_ai_instance = MagicMock()
            mock_ai_service.return_value = mock_ai_instance
            mock_ai_instance.get_conversation_log.side_effect = Exception("File system error")
            
            response = client.get(f"/api/cases/{case_id}/ai-conversations")
            
            assert response.status_code == 500
            data = response.json()
            assert "Failed to retrieve conversation log" in data["detail"]


class TestAIAnalysisDataStorage:
    """Test class for AI analysis data storage and retrieval functionality"""
    
    def test_analysis_data_persistence(self, client, sample_case_data):
        """Test that analysis data is properly stored and can be retrieved"""
        case_id = "case-001"
        
        with patch('app.api.cases.CasesService.load_cases') as mock_load_cases, \
             patch('app.api.cases.AIAnalysisService') as mock_ai_service:
            
            mock_load_cases.return_value = [{"id": case_id, **sample_case_data}]
            mock_ai_instance = MagicMock()
            mock_ai_service.return_value = mock_ai_instance
            
            # Mock analysis result
            analysis_result = {
                "case_id": case_id,
                "timestamp": "2024-01-15T10:00:00Z",
                "claim_reference": "CLM-2024-001",
                "key_facts": ["Fact 1", "Fact 2"]
            }
            
            # Test POST (trigger analysis)
            mock_ai_instance.analyze_case.return_value = analysis_result
            post_response = client.post(f"/api/cases/{case_id}/ai-analysis")
            assert post_response.status_code == 200
            
            # Test GET (retrieve analysis)
            mock_ai_instance.get_case_analysis.return_value = analysis_result
            get_response = client.get(f"/api/cases/{case_id}/ai-analysis")
            assert get_response.status_code == 200
            
            get_data = get_response.json()
            assert get_data["analysis"] == analysis_result
    
    def test_conversation_logging_workflow(self, client, sample_case_data):
        """Test that conversations are logged during analysis and can be retrieved"""
        case_id = "case-001"
        
        with patch('app.api.cases.CasesService.load_cases') as mock_load_cases, \
             patch('app.api.cases.AIAnalysisService') as mock_ai_service:
            
            mock_load_cases.return_value = [{"id": case_id, **sample_case_data}]
            mock_ai_instance = MagicMock()
            mock_ai_service.return_value = mock_ai_instance
            
            # Mock analysis (which should log conversation)
            analysis_result = {"case_id": case_id, "key_facts": ["Fact 1"]}
            mock_ai_instance.analyze_case.return_value = analysis_result
            
            # Trigger analysis
            analysis_response = client.post(f"/api/cases/{case_id}/ai-analysis")
            assert analysis_response.status_code == 200
            
            # Mock conversation log retrieval
            expected_conversations = [
                {
                    "id": "conv-001",
                    "timestamp": "2024-01-15T10:00:00Z",
                    "analysis_type": "case_analysis",
                    "prompt": "Analyze case documents...",
                    "response": "Analysis complete..."
                }
            ]
            mock_ai_instance.get_conversation_log.return_value = expected_conversations
            
            # Retrieve conversations
            conv_response = client.get(f"/api/cases/{case_id}/ai-conversations")
            assert conv_response.status_code == 200
            
            conv_data = conv_response.json()
            assert conv_data["conversations"] == expected_conversations
            assert conv_data["total_conversations"] == 1


class TestAIAnalysisErrorScenarios:
    """Test class for various error scenarios in AI analysis endpoints"""
    
    def test_malformed_case_id(self, client):
        """Test endpoints with malformed case IDs"""
        malformed_ids = ["", "case with spaces", "case/with/slashes"]
        
        for case_id in malformed_ids:
            # Test all three endpoints
            post_response = client.post(f"/api/cases/{case_id}/ai-analysis")
            get_analysis_response = client.get(f"/api/cases/{case_id}/ai-analysis")
            get_conv_response = client.get(f"/api/cases/{case_id}/ai-conversations")
            
            # All should handle gracefully (either 404 or 422)
            assert post_response.status_code in [404, 422]
            assert get_analysis_response.status_code in [404, 422]
            assert get_conv_response.status_code in [404, 422]
    
    def test_service_unavailable_scenarios(self, client, sample_case_data):
        """Test behavior when underlying services are unavailable"""
        case_id = "case-001"
        
        # Test when CasesService fails
        with patch('app.api.cases.CasesService.load_cases') as mock_load_cases:
            mock_load_cases.side_effect = Exception("Database unavailable")
            
            response = client.post(f"/api/cases/{case_id}/ai-analysis")
            assert response.status_code == 500
            assert "Failed to perform AI analysis" in response.json()["detail"]
        
        # Test when AIAnalysisService fails to initialize
        with patch('app.api.cases.CasesService.load_cases') as mock_load_cases, \
             patch('app.api.cases.AIAnalysisService') as mock_ai_service:
            
            mock_load_cases.return_value = [{"id": case_id, **sample_case_data}]
            mock_ai_service.side_effect = Exception("AI service initialization failed")
            
            response = client.post(f"/api/cases/{case_id}/ai-analysis")
            assert response.status_code == 500