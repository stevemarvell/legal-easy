#!/usr/bin/env python3
"""
Unit tests for AIAnalysisService
"""

import pytest
import json
from unittest.mock import patch, mock_open, MagicMock
from pathlib import Path
from datetime import datetime, timezone

from app.services.ai_analysis_service import AIAnalysisService


class TestAIAnalysisService:
    """Test cases for AIAnalysisService"""

    @pytest.fixture
    @patch.dict('os.environ', {'CLAUDE_API_KEY': 'test-key'})
    @patch('app.services.ai_analysis_service.ClaudeClient')
    @patch('app.services.ai_analysis_service.DocumentExtractor')
    def ai_service(self, mock_doc_extractor, mock_claude_client):
        """Create AIAnalysisService instance for testing"""
        return AIAnalysisService()

    @pytest.fixture
    def mock_case_data(self):
        """Mock case data for testing"""
        return {
            "id": "case-001",
            "title": "Test Case",
            "case_type": "Employment Dispute",
            "client_name": "John Doe",
            "summary": "Test case summary",
            "documents": ["doc-001", "doc-002"],
            "playbook_id": "employment-dispute"
        }

    @pytest.fixture
    def mock_analysis_response(self):
        """Mock Claude API response for testing"""
        return json.dumps({
            "caseId": "case-001",
            "timestamp": "2024-01-15T10:30:00Z",
            "claimReference": "REF-001",
            "claimantName": "John Doe",
            "keyFacts": ["Fact 1", "Fact 2"],
            "confidence": 0.85
        })

    @patch('app.services.ai_analysis_service.ClaudeClient')
    @patch('app.services.ai_analysis_service.DocumentExtractor')
    def test_init(self, mock_doc_extractor, mock_claude_client):
        """Test AIAnalysisService initialization"""
        service = AIAnalysisService()
        
        assert service.claude_client is not None
        assert service.document_extractor is not None
        assert service.backend_dir is not None
        assert service.ai_data_dir is not None

    @patch('app.services.ai_analysis_service.AIAnalysisService._load_case_data')
    @patch('app.services.ai_analysis_service.AIAnalysisService._extract_case_documents')
    @patch('app.services.ai_analysis_service.AIAnalysisService._store_analysis_result')
    @patch('app.services.ai_analysis_service.AIAnalysisService._log_conversation')
    def test_analyze_case_success(self, mock_log, mock_store, mock_extract_docs, 
                                 mock_load_case, ai_service, mock_case_data, mock_analysis_response):
        """Test successful case analysis"""
        # Setup mocks
        mock_load_case.return_value = mock_case_data
        mock_extract_docs.return_value = [
            {"document_id": "doc-001", "content": "Document content 1"},
            {"document_id": "doc-002", "content": "Document content 2"}
        ]
        ai_service.claude_client.analyze_case.return_value = mock_analysis_response
        
        # Execute
        result = ai_service.analyze_case("case-001")
        
        # Verify
        assert result["caseId"] == "case-001"
        assert result["claimReference"] == "REF-001"
        assert result["keyFacts"] == ["Fact 1", "Fact 2"]
        assert result["confidence"] == 0.85
        
        mock_load_case.assert_called_once_with("case-001")
        mock_extract_docs.assert_called_once_with("case-001", ["doc-001", "doc-002"])
        mock_store.assert_called_once()
        mock_log.assert_called_once()

    @patch('app.services.ai_analysis_service.AIAnalysisService._load_case_data')
    def test_analyze_case_case_not_found(self, mock_load_case, ai_service):
        """Test case analysis when case is not found"""
        mock_load_case.return_value = None
        
        with pytest.raises(ValueError, match="Case case-001 not found"):
            ai_service.analyze_case("case-001")

    @patch('app.services.ai_analysis_service.AIAnalysisService._load_case_data')
    @patch('app.services.ai_analysis_service.AIAnalysisService._extract_case_documents')
    def test_analyze_case_no_documents(self, mock_extract_docs, mock_load_case, 
                                      ai_service, mock_case_data):
        """Test case analysis when no documents are found"""
        mock_load_case.return_value = mock_case_data
        mock_extract_docs.return_value = []
        
        with pytest.raises(ValueError, match="No documents found for case case-001"):
            ai_service.analyze_case("case-001")

    @patch("builtins.open", new_callable=mock_open, read_data='{"caseId": "case-001", "keyFacts": ["fact1"]}')
    @patch("pathlib.Path.exists", return_value=True)
    def test_get_case_analysis_success(self, mock_exists, mock_file, ai_service):
        """Test successful retrieval of case analysis"""
        result = ai_service.get_case_analysis("case-001")
        
        assert result is not None
        assert result["caseId"] == "case-001"
        assert result["keyFacts"] == ["fact1"]

    @patch("pathlib.Path.exists", return_value=False)
    def test_get_case_analysis_not_found(self, mock_exists, ai_service):
        """Test case analysis retrieval when file doesn't exist"""
        result = ai_service.get_case_analysis("case-001")
        
        assert result is None

    @patch("builtins.open", side_effect=Exception("File error"))
    @patch("pathlib.Path.exists", return_value=True)
    def test_get_case_analysis_exception(self, mock_exists, mock_file, ai_service):
        """Test case analysis retrieval with exception"""
        result = ai_service.get_case_analysis("case-001")
        
        assert result is None

    @patch("builtins.open", new_callable=mock_open, read_data='{"conversations": [{"id": "1", "timestamp": "2024-01-01"}]}')
    @patch("pathlib.Path.exists", return_value=True)
    def test_get_conversation_log_success(self, mock_exists, mock_file, ai_service):
        """Test successful retrieval of conversation log"""
        result = ai_service.get_conversation_log("case-001")
        
        assert len(result) == 1
        assert result[0]["id"] == "1"
        assert result[0]["timestamp"] == "2024-01-01"

    @patch("pathlib.Path.exists", return_value=False)
    def test_get_conversation_log_not_found(self, mock_exists, ai_service):
        """Test conversation log retrieval when file doesn't exist"""
        result = ai_service.get_conversation_log("case-001")
        
        assert result == []

    @patch("builtins.open", new_callable=mock_open, read_data='[{"id": "case-001", "title": "Test"}]')
    @patch("pathlib.Path.exists", return_value=True)
    def test_load_case_data_success(self, mock_exists, mock_file, ai_service):
        """Test successful case data loading"""
        result = ai_service._load_case_data("case-001")
        
        assert result is not None
        assert result["id"] == "case-001"

    @patch("pathlib.Path.exists", return_value=False)
    def test_load_case_data_file_not_found(self, mock_exists, ai_service):
        """Test case data loading when file doesn't exist"""
        result = ai_service._load_case_data("case-001")
        
        assert result is None

    def test_create_analysis_prompt(self, ai_service, mock_case_data):
        """Test analysis prompt creation"""
        document_texts = [
            {"document_id": "doc-001", "content": "Content 1"},
            {"document_id": "doc-002", "content": "Content 2"}
        ]
        
        prompt = ai_service._create_analysis_prompt(mock_case_data, document_texts)
        
        assert "case-001" in prompt
        assert "Test Case" in prompt
        assert "Employment Dispute" in prompt
        assert "John Doe" in prompt
        assert "Content 1" in prompt
        assert "Content 2" in prompt
        assert "JSON response" in prompt

    def test_parse_analysis_response_success(self, ai_service, mock_analysis_response):
        """Test successful analysis response parsing"""
        result = ai_service._parse_analysis_response("case-001", mock_analysis_response)
        
        assert result["caseId"] == "case-001"
        assert result["claimReference"] == "REF-001"
        assert result["keyFacts"] == ["Fact 1", "Fact 2"]
        assert "timestamp" in result

    def test_parse_analysis_response_invalid_json(self, ai_service):
        """Test analysis response parsing with invalid JSON"""
        invalid_response = "This is not JSON"
        
        result = ai_service._parse_analysis_response("case-001", invalid_response)
        
        assert result["caseId"] == "case-001"
        assert result["error"] == "Failed to parse AI response"
        assert result["rawResponse"] == invalid_response
        assert result["confidence"] == 0.0

    @patch("builtins.open", new_callable=mock_open)
    @patch("pathlib.Path.mkdir")
    def test_store_analysis_result(self, mock_mkdir, mock_file, ai_service):
        """Test storing analysis result"""
        analysis_result = {"caseId": "case-001", "keyFacts": ["fact1"]}
        
        ai_service._store_analysis_result("case-001", analysis_result)
        
        mock_mkdir.assert_called_once()
        mock_file.assert_called_once()

    @patch("builtins.open", new_callable=mock_open, read_data='{"conversations": []}')
    @patch("pathlib.Path.mkdir")
    @patch("pathlib.Path.exists", return_value=False)
    def test_log_conversation_new_file(self, mock_exists, mock_mkdir, mock_file, ai_service):
        """Test logging conversation to new file"""
        ai_service._log_conversation("case-001", "prompt", "response", "case_analysis")
        
        mock_mkdir.assert_called_once()
        # Should be called once for writing (reading fails because file doesn't exist)
        assert mock_file.call_count == 1

    @patch("builtins.open", new_callable=mock_open, read_data='{"conversations": [{"id": "existing"}]}')
    @patch("pathlib.Path.mkdir")
    @patch("pathlib.Path.exists", return_value=True)
    def test_log_conversation_existing_file(self, mock_exists, mock_mkdir, mock_file, ai_service):
        """Test logging conversation to existing file"""
        ai_service._log_conversation("case-001", "prompt", "response", "case_analysis")
        
        mock_mkdir.assert_called_once()
        # Should be called twice - once for reading, once for writing
        assert mock_file.call_count == 2

    @patch('app.services.ai_analysis_service.AIAnalysisService._load_case_data')
    @patch('app.services.ai_analysis_service.AIAnalysisService._extract_case_documents')
    @patch('app.services.ai_analysis_service.AIAnalysisService._log_conversation')
    def test_analyze_case_claude_api_error(self, mock_log, mock_extract_docs, 
                                          mock_load_case, ai_service, mock_case_data):
        """Test case analysis when Claude API fails"""
        # Setup mocks
        mock_load_case.return_value = mock_case_data
        mock_extract_docs.return_value = [
            {"document_id": "doc-001", "content": "Document content 1"}
        ]
        ai_service.claude_client.analyze_case.side_effect = Exception("API Error")
        
        # Execute and verify exception is raised
        with pytest.raises(Exception, match="API Error"):
            ai_service.analyze_case("case-001")
        
        # Verify error conversation is logged
        mock_log.assert_called_once()
        args = mock_log.call_args[0]
        assert args[0] == "case-001"  # case_id
        assert "Error: API Error" in args[2]  # response contains error
        assert args[3] == "case_analysis"  # analysis_type
        assert mock_log.call_args[1]['success'] is False  # success=False

    @patch('app.services.ai_analysis_service.AIAnalysisService._load_case_data')
    @patch('app.services.ai_analysis_service.AIAnalysisService._extract_case_documents')
    def test_analyze_case_document_extraction_error(self, mock_extract_docs, 
                                                   mock_load_case, ai_service, mock_case_data):
        """Test case analysis when document extraction fails"""
        mock_load_case.return_value = mock_case_data
        mock_extract_docs.side_effect = Exception("Document extraction failed")
        
        with pytest.raises(Exception, match="Document extraction failed"):
            ai_service.analyze_case("case-001")

    @patch("builtins.open", side_effect=Exception("File write error"))
    @patch("pathlib.Path.mkdir")
    def test_store_analysis_result_error(self, mock_mkdir, mock_file, ai_service):
        """Test storing analysis result with file write error"""
        analysis_result = {"caseId": "case-001", "keyFacts": ["fact1"]}
        
        with pytest.raises(Exception, match="File write error"):
            ai_service._store_analysis_result("case-001", analysis_result)

    @patch("builtins.open", side_effect=Exception("Conversation log error"))
    @patch("pathlib.Path.mkdir")
    def test_log_conversation_error_handling(self, mock_mkdir, mock_file, ai_service):
        """Test conversation logging with file error - should not raise"""
        # This should not raise an exception as logging is non-critical
        ai_service._log_conversation("case-001", "prompt", "response", "case_analysis")
        
        # Verify mkdir was still called
        mock_mkdir.assert_called_once()

    def test_extract_case_documents_partial_failure(self, ai_service):
        """Test document extraction with some documents failing"""
        document_ids = ["doc-001", "doc-002", "doc-003"]
        
        # Mock document extractor to fail on second document
        def mock_extract_side_effect(case_id, doc_id):
            if doc_id == "doc-002":
                raise Exception("Document extraction failed")
            return f"Content for {doc_id}"
        
        ai_service.document_extractor.extract_text.side_effect = mock_extract_side_effect
        
        result = ai_service._extract_case_documents("case-001", document_ids)
        
        # Should return only successful extractions
        assert len(result) == 2
        assert result[0]["document_id"] == "doc-001"
        assert result[0]["content"] == "Content for doc-001"
        assert result[1]["document_id"] == "doc-003"
        assert result[1]["content"] == "Content for doc-003"

    def test_parse_analysis_response_partial_json(self, ai_service):
        """Test parsing response with partial/incomplete JSON"""
        incomplete_response = '{"caseId": "case-001", "keyFacts": ["fact1"]'  # Missing closing brace
        
        result = ai_service._parse_analysis_response("case-001", incomplete_response)
        
        assert result["caseId"] == "case-001"
        assert result["error"] == "Failed to parse AI response"
        assert result["rawResponse"] == incomplete_response
        assert result["confidence"] == 0.0

    def test_parse_analysis_response_missing_optional_fields(self, ai_service):
        """Test parsing response with missing optional fields"""
        minimal_response = json.dumps({
            "caseId": "case-001",
            "keyFacts": ["fact1", "fact2"]
        })
        
        result = ai_service._parse_analysis_response("case-001", minimal_response)
        
        assert result["caseId"] == "case-001"
        assert result["keyFacts"] == ["fact1", "fact2"]
        assert "timestamp" in result
        # Optional fields should be None or empty
        assert result.get("claimReference") is None
        assert result.get("claimAmount") is None

    @patch("builtins.open", new_callable=mock_open, read_data='invalid json')
    @patch("pathlib.Path.exists", return_value=True)
    def test_get_case_analysis_invalid_json(self, mock_exists, mock_file, ai_service):
        """Test retrieving case analysis with invalid JSON"""
        result = ai_service.get_case_analysis("case-001")
        
        assert result is None

    @patch("builtins.open", new_callable=mock_open, read_data='invalid json')
    @patch("pathlib.Path.exists", return_value=True)
    def test_get_conversation_log_invalid_json(self, mock_exists, mock_file, ai_service):
        """Test retrieving conversation log with invalid JSON"""
        result = ai_service.get_conversation_log("case-001")
        
        assert result == []

    @patch("builtins.open", new_callable=mock_open, read_data='[{"id": "case-002"}]')
    @patch("pathlib.Path.exists", return_value=True)
    def test_load_case_data_case_not_in_list(self, mock_exists, mock_file, ai_service):
        """Test loading case data when case ID is not in the list"""
        result = ai_service._load_case_data("case-001")
        
        assert result is None

    @patch("builtins.open", side_effect=Exception("File read error"))
    @patch("pathlib.Path.exists", return_value=True)
    def test_load_case_data_file_read_error(self, mock_exists, mock_file, ai_service):
        """Test loading case data with file read error"""
        result = ai_service._load_case_data("case-001")
        
        assert result is None

    def test_create_analysis_prompt_empty_documents(self, ai_service, mock_case_data):
        """Test creating analysis prompt with empty document list"""
        document_texts = []
        
        prompt = ai_service._create_analysis_prompt(mock_case_data, document_texts)
        
        assert "case-001" in prompt
        assert "Test Case" in prompt
        assert "JSON response" in prompt
        # Should handle empty documents gracefully
        assert "Documents to analyze:" in prompt