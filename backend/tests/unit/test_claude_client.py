#!/usr/bin/env python3
"""
Unit tests for ClaudeClient
"""

import pytest
import json
import time
from unittest.mock import patch, MagicMock
import requests

from app.services.claude_client import ClaudeClient, ClaudeAPIError, ClaudeRateLimitError


class TestClaudeClient:
    """Test cases for ClaudeClient"""

    @patch.dict('os.environ', {'CLAUDE_API_KEY': 'test-key'})
    def test_init_with_api_key(self):
        """Test ClaudeClient initialization with API key"""
        client = ClaudeClient()
        
        assert client.api_key == 'test-key'
        assert client.model == 'claude-3-sonnet-20240229'
        assert client.max_tokens == 4000
        assert client.session is not None

    def test_init_without_api_key(self):
        """Test ClaudeClient initialization without API key"""
        with patch.dict('os.environ', {}, clear=True):
            with pytest.raises(ValueError, match="CLAUDE_API_KEY environment variable is required"):
                ClaudeClient()

    @patch.dict('os.environ', {
        'CLAUDE_API_KEY': 'test-key',
        'CLAUDE_MODEL': 'custom-model',
        'CLAUDE_MAX_TOKENS': '2000',
        'CLAUDE_RATE_LIMIT_RPM': '30'
    })
    def test_init_with_custom_config(self):
        """Test ClaudeClient initialization with custom configuration"""
        client = ClaudeClient()
        
        assert client.model == 'custom-model'
        assert client.max_tokens == 2000
        assert client.rate_limit_requests_per_minute == 30

    @patch.dict('os.environ', {'CLAUDE_API_KEY': 'test-key'})
    @patch('requests.Session.post')
    def test_analyze_case_success(self, mock_post):
        """Test successful case analysis"""
        # Setup mock response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'content': [{'text': '{"result": "success"}'}],
            'usage': {'input_tokens': 100, 'output_tokens': 50}
        }
        mock_post.return_value = mock_response
        
        client = ClaudeClient()
        result = client.analyze_case("Test prompt")
        
        assert result == '{"result": "success"}'
        mock_post.assert_called_once()

    @patch.dict('os.environ', {'CLAUDE_API_KEY': 'test-key'})
    @patch('requests.Session.post')
    def test_analyze_case_rate_limit(self, mock_post):
        """Test case analysis with rate limit error"""
        # Setup mock response
        mock_response = MagicMock()
        mock_response.status_code = 429
        mock_response.headers = {'retry-after': '60'}
        mock_post.return_value = mock_response
        
        client = ClaudeClient()
        
        with pytest.raises(ClaudeRateLimitError):
            client.analyze_case("Test prompt")

    @patch.dict('os.environ', {'CLAUDE_API_KEY': 'test-key'})
    @patch('requests.Session.post')
    def test_analyze_case_server_error(self, mock_post):
        """Test case analysis with server error"""
        # Setup mock response
        mock_response = MagicMock()
        mock_response.status_code = 500
        mock_response.text = "Internal Server Error"
        mock_post.return_value = mock_response
        
        client = ClaudeClient()
        
        with pytest.raises(ClaudeAPIError, match="Server error 500"):
            client.analyze_case("Test prompt")

    @patch.dict('os.environ', {'CLAUDE_API_KEY': 'test-key'})
    @patch('requests.Session.post')
    def test_analyze_case_auth_error(self, mock_post):
        """Test case analysis with authentication error"""
        # Setup mock response
        mock_response = MagicMock()
        mock_response.status_code = 401
        mock_post.return_value = mock_response
        
        client = ClaudeClient()
        
        with pytest.raises(ClaudeAPIError, match="Authentication failed"):
            client.analyze_case("Test prompt")

    @patch.dict('os.environ', {'CLAUDE_API_KEY': 'test-key'})
    @patch('requests.Session.post')
    def test_analyze_case_bad_request(self, mock_post):
        """Test case analysis with bad request error"""
        # Setup mock response
        mock_response = MagicMock()
        mock_response.status_code = 400
        mock_response.headers = {'content-type': 'application/json'}
        mock_response.json.return_value = {
            'error': {'message': 'Invalid request format'}
        }
        mock_post.return_value = mock_response
        
        client = ClaudeClient()
        
        with pytest.raises(ClaudeAPIError, match="Bad request: Invalid request format"):
            client.analyze_case("Test prompt")

    @patch.dict('os.environ', {'CLAUDE_API_KEY': 'test-key'})
    @patch('requests.Session.post')
    def test_analyze_case_timeout(self, mock_post):
        """Test case analysis with timeout"""
        mock_post.side_effect = requests.exceptions.Timeout()
        
        client = ClaudeClient()
        
        with pytest.raises(ClaudeAPIError, match="Request timeout"):
            client.analyze_case("Test prompt")

    @patch.dict('os.environ', {'CLAUDE_API_KEY': 'test-key'})
    @patch('requests.Session.post')
    def test_analyze_case_connection_error(self, mock_post):
        """Test case analysis with connection error"""
        mock_post.side_effect = requests.exceptions.ConnectionError()
        
        client = ClaudeClient()
        
        with pytest.raises(ClaudeAPIError, match="Connection error"):
            client.analyze_case("Test prompt")

    @patch.dict('os.environ', {'CLAUDE_API_KEY': 'test-key'})
    def test_check_rate_limits_within_limits(self):
        """Test rate limit checking when within limits"""
        client = ClaudeClient()
        
        # Should not raise any exception
        client._check_rate_limits()

    @patch.dict('os.environ', {'CLAUDE_API_KEY': 'test-key', 'CLAUDE_RATE_LIMIT_RPM': '2'})
    def test_check_rate_limits_request_limit_exceeded(self):
        """Test rate limit checking when request limit is exceeded"""
        client = ClaudeClient()
        
        # Add requests to exceed limit
        current_time = time.time()
        client.request_times = [current_time - 30, current_time - 20, current_time - 10]
        
        with pytest.raises(ClaudeRateLimitError, match="Request rate limit exceeded"):
            client._check_rate_limits()

    @patch.dict('os.environ', {'CLAUDE_API_KEY': 'test-key', 'CLAUDE_RATE_LIMIT_TPM': '100'})
    def test_check_rate_limits_token_limit_exceeded(self):
        """Test rate limit checking when token limit is exceeded"""
        client = ClaudeClient()
        
        # Add token usage to exceed limit
        current_time = time.time()
        client.token_usage = [
            {'time': current_time - 30, 'tokens': 60},
            {'time': current_time - 20, 'tokens': 50}
        ]
        
        with pytest.raises(ClaudeRateLimitError, match="Token rate limit exceeded"):
            client._check_rate_limits()

    @patch.dict('os.environ', {'CLAUDE_API_KEY': 'test-key'})
    @patch('requests.Session.post')
    @patch('time.sleep')  # Mock sleep to speed up tests
    def test_make_request_with_backoff_retry_success(self, mock_sleep, mock_post):
        """Test request with backoff that succeeds on retry"""
        # First call fails with 500, second succeeds
        mock_response_fail = MagicMock()
        mock_response_fail.status_code = 500
        mock_response_fail.text = "Server Error"
        
        mock_response_success = MagicMock()
        mock_response_success.status_code = 200
        mock_response_success.json.return_value = {'content': [{'text': 'success'}]}
        
        mock_post.side_effect = [mock_response_fail, mock_response_success]
        
        client = ClaudeClient()
        payload = {'test': 'data'}
        
        result = client._make_request_with_backoff(payload)
        
        assert result == {'content': [{'text': 'success'}]}
        assert mock_post.call_count == 2
        mock_sleep.assert_called_once()

    @patch.dict('os.environ', {'CLAUDE_API_KEY': 'test-key'})
    def test_validate_response_valid_json(self):
        """Test response validation with valid JSON"""
        client = ClaudeClient()
        valid_response = '{"caseId": "case-001", "keyFacts": ["fact1"]}'
        
        result = client.validate_response(valid_response)
        
        assert result is True

    @patch.dict('os.environ', {'CLAUDE_API_KEY': 'test-key'})
    def test_validate_response_invalid_json(self):
        """Test response validation with invalid JSON"""
        client = ClaudeClient()
        invalid_response = 'This is not JSON'
        
        result = client.validate_response(invalid_response)
        
        assert result is False

    @patch.dict('os.environ', {'CLAUDE_API_KEY': 'test-key'})
    def test_validate_response_missing_required_fields(self):
        """Test response validation with missing required fields"""
        client = ClaudeClient()
        incomplete_response = '{"caseId": "case-001"}'  # Missing keyFacts
        
        result = client.validate_response(incomplete_response)
        
        assert result is False

    @patch.dict('os.environ', {'CLAUDE_API_KEY': 'test-key'})
    def test_get_api_status(self):
        """Test getting API status"""
        client = ClaudeClient()
        
        # Add some mock data
        current_time = time.time()
        client.request_times = [current_time - 30]
        client.token_usage = [{'time': current_time - 20, 'tokens': 100}]
        
        status = client.get_api_status()
        
        assert status['api_configured'] is True
        assert status['requests_in_last_minute'] == 1
        assert status['tokens_in_last_minute'] == 100
        assert status['model'] == 'claude-3-sonnet-20240229'
        assert status['max_tokens'] == 4000

    @patch.dict('os.environ', {'CLAUDE_API_KEY': 'test-key'})
    @patch('requests.Session.post')
    def test_analyze_case_invalid_response_format(self, mock_post):
        """Test case analysis with invalid response format"""
        # Setup mock response with missing content
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {'usage': {'input_tokens': 100}}  # Missing content
        mock_post.return_value = mock_response
        
        client = ClaudeClient()
        
        with pytest.raises(ClaudeAPIError, match="Invalid response format"):
            client.analyze_case("Test prompt")

    @patch.dict('os.environ', {'CLAUDE_API_KEY': 'test-key'})
    @patch('requests.Session.post')
    def test_analyze_case_empty_content(self, mock_post):
        """Test case analysis with empty content array"""
        # Setup mock response with empty content
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'content': [],  # Empty content array
            'usage': {'input_tokens': 100, 'output_tokens': 0}
        }
        mock_post.return_value = mock_response
        
        client = ClaudeClient()
        
        with pytest.raises(ClaudeAPIError, match="Invalid response format"):
            client.analyze_case("Test prompt")

    @patch.dict('os.environ', {'CLAUDE_API_KEY': 'test-key'})
    @patch('requests.Session.post')
    def test_analyze_case_json_decode_error(self, mock_post):
        """Test case analysis with JSON decode error"""
        mock_post.side_effect = requests.exceptions.JSONDecodeError("Invalid JSON", "", 0)
        
        client = ClaudeClient()
        
        with pytest.raises(ClaudeAPIError, match="Invalid JSON response"):
            client.analyze_case("Test prompt")

    @patch.dict('os.environ', {'CLAUDE_API_KEY': 'test-key'})
    @patch('requests.Session.post')
    def test_analyze_case_unexpected_status_code(self, mock_post):
        """Test case analysis with unexpected status code"""
        mock_response = MagicMock()
        mock_response.status_code = 418  # I'm a teapot
        mock_response.text = "I'm a teapot"
        mock_post.return_value = mock_response
        
        client = ClaudeClient()
        
        with pytest.raises(ClaudeAPIError, match="Unexpected status code 418"):
            client.analyze_case("Test prompt")

    @patch.dict('os.environ', {'CLAUDE_API_KEY': 'test-key'})
    @patch('requests.Session.post')
    @patch('time.sleep')
    def test_make_request_with_backoff_max_retries_exceeded(self, mock_sleep, mock_post):
        """Test request with backoff when max retries are exceeded"""
        # All requests fail with 500
        mock_response = MagicMock()
        mock_response.status_code = 500
        mock_response.text = "Server Error"
        mock_post.return_value = mock_response
        
        client = ClaudeClient()
        payload = {'test': 'data'}
        
        with pytest.raises(ClaudeAPIError, match="Server error 500"):
            client._make_request_with_backoff(payload, max_retries=2)
        
        # Should have made 3 attempts (initial + 2 retries)
        assert mock_post.call_count == 3

    @patch.dict('os.environ', {'CLAUDE_API_KEY': 'test-key'})
    @patch('requests.Session.post')
    @patch('time.sleep')
    def test_make_request_with_backoff_timeout_retries(self, mock_sleep, mock_post):
        """Test request with backoff for timeout errors"""
        # All requests timeout
        mock_post.side_effect = requests.exceptions.Timeout()
        
        client = ClaudeClient()
        payload = {'test': 'data'}
        
        with pytest.raises(ClaudeAPIError, match="Request timeout, max retries reached"):
            client._make_request_with_backoff(payload, max_retries=1)
        
        # Should have made 2 attempts (initial + 1 retry)
        assert mock_post.call_count == 2

    @patch.dict('os.environ', {'CLAUDE_API_KEY': 'test-key'})
    @patch('requests.Session.post')
    @patch('time.sleep')
    def test_make_request_with_backoff_connection_retries(self, mock_sleep, mock_post):
        """Test request with backoff for connection errors"""
        # All requests fail with connection error
        mock_post.side_effect = requests.exceptions.ConnectionError()
        
        client = ClaudeClient()
        payload = {'test': 'data'}
        
        with pytest.raises(ClaudeAPIError, match="Connection error, max retries reached"):
            client._make_request_with_backoff(payload, max_retries=1)
        
        # Should have made 2 attempts (initial + 1 retry)
        assert mock_post.call_count == 2

    @patch.dict('os.environ', {'CLAUDE_API_KEY': 'test-key'})
    def test_validate_response_empty_string(self):
        """Test response validation with empty string"""
        client = ClaudeClient()
        
        result = client.validate_response("")
        
        assert result is False

    @patch.dict('os.environ', {'CLAUDE_API_KEY': 'test-key'})
    def test_validate_response_null_values(self):
        """Test response validation with null values in required fields"""
        client = ClaudeClient()
        response_with_nulls = '{"caseId": null, "keyFacts": null}'
        
        result = client.validate_response(response_with_nulls)
        
        # Should still be valid as the fields exist, even if null
        assert result is True

    @patch.dict('os.environ', {'CLAUDE_API_KEY': 'test-key'})
    def test_check_rate_limits_old_requests_cleanup(self):
        """Test that old request times are properly cleaned up"""
        client = ClaudeClient()
        
        # Add old request times (older than 1 minute)
        current_time = time.time()
        client.request_times = [current_time - 120, current_time - 90, current_time - 30]
        client.token_usage = [
            {'time': current_time - 120, 'tokens': 100},
            {'time': current_time - 30, 'tokens': 50}
        ]
        
        # This should clean up old entries and not raise
        client._check_rate_limits()
        
        # Only recent entries should remain
        assert len(client.request_times) == 1
        assert len(client.token_usage) == 1

    @patch.dict('os.environ', {'CLAUDE_API_KEY': 'test-key'})
    def test_get_api_status_no_usage_data(self):
        """Test getting API status with no usage data"""
        client = ClaudeClient()
        
        status = client.get_api_status()
        
        assert status['api_configured'] is True
        assert status['requests_in_last_minute'] == 0
        assert status['tokens_in_last_minute'] == 0