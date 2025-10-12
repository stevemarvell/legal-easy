#!/usr/bin/env python3
"""
Claude API Client - Secure client for Claude API integration

This client handles:
- Secure authentication with Claude API
- Rate limiting and exponential backoff retry logic
- Structured prompt generation and response validation
- Error handling for API failures
"""

import os
import time
import json
import logging
from typing import Dict, Any, Optional
from datetime import datetime, timezone
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


logger = logging.getLogger(__name__)


class ClaudeAPIError(Exception):
    """Custom exception for Claude API errors."""
    pass


class ClaudeRateLimitError(ClaudeAPIError):
    """Exception for rate limit errors."""
    pass


class ClaudeClient:
    """Client for interacting with Claude API."""
    
    def __init__(self):
        """Initialize the Claude API client."""
        # Ensure environment variables are loaded
        from dotenv import load_dotenv
        from pathlib import Path
        
        # Load .env file from the backend directory
        backend_dir = Path(__file__).parent.parent.parent
        env_path = backend_dir / '.env'
        load_dotenv(env_path)
        
        self.api_key = os.getenv('CLAUDE_API_KEY')
        self.api_url = os.getenv('CLAUDE_API_URL', 'https://api.anthropic.com/v1/messages')
        self.model = os.getenv('CLAUDE_MODEL', 'claude-3-sonnet-20240229')
        self.max_tokens = int(os.getenv('CLAUDE_MAX_TOKENS', '4000'))
        
        if not self.api_key:
            raise ValueError("CLAUDE_API_KEY environment variable is required")
        
        # Rate limiting configuration
        self.rate_limit_requests_per_minute = int(os.getenv('CLAUDE_RATE_LIMIT_RPM', '50'))
        self.rate_limit_tokens_per_minute = int(os.getenv('CLAUDE_RATE_LIMIT_TPM', '40000'))
        
        # Request tracking for rate limiting
        self.request_times = []
        self.token_usage = []
        
        # Setup HTTP session with retry strategy
        self.session = requests.Session()
        retry_strategy = Retry(
            total=3,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["HEAD", "GET", "POST"],
            backoff_factor=1
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        self.session.mount("http://", adapter)
        self.session.mount("https://", adapter)
        
        # Set default headers
        self.session.headers.update({
            'Content-Type': 'application/json',
            'x-api-key': self.api_key,
            'anthropic-version': '2023-06-01'
        })
    
    def analyze_case(self, prompt: str) -> str:
        """
        Send case analysis request to Claude API.
        
        Args:
            prompt: The analysis prompt to send
            
        Returns:
            The API response as a string
            
        Raises:
            ClaudeAPIError: If the API request fails
            ClaudeRateLimitError: If rate limits are exceeded
        """
        try:
            logger.info("Sending case analysis request to Claude API")
            
            # Check rate limits before making request
            self._check_rate_limits()
            
            # Prepare request payload
            payload = {
                "model": self.model,
                "max_tokens": self.max_tokens,
                "messages": [
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                "temperature": 0.1,  # Low temperature for consistent analysis
                "system": "You are a legal AI assistant that analyzes case documents and extracts structured information. Always respond with valid JSON format."
            }
            
            # Make request with exponential backoff
            response = self._make_request_with_backoff(payload)
            
            # Extract content from response
            if 'content' in response and len(response['content']) > 0:
                content = response['content'][0].get('text', '')
                logger.info("Successfully received response from Claude API")
                return content
            else:
                raise ClaudeAPIError("Invalid response format from Claude API")
                
        except ClaudeRateLimitError:
            raise
        except ClaudeAPIError:
            raise
        except Exception as e:
            logger.error(f"Unexpected error in Claude API request: {str(e)}")
            raise ClaudeAPIError(f"Unexpected error: {str(e)}")
    
    def _check_rate_limits(self) -> None:
        """Check if we're within rate limits."""
        current_time = time.time()
        
        # Clean old request times (older than 1 minute)
        self.request_times = [t for t in self.request_times if current_time - t < 60]
        self.token_usage = [t for t in self.token_usage if current_time - t['time'] < 60]
        
        # Check request rate limit
        if len(self.request_times) >= self.rate_limit_requests_per_minute:
            wait_time = 60 - (current_time - self.request_times[0])
            if wait_time > 0:
                logger.warning(f"Rate limit reached, waiting {wait_time:.2f} seconds")
                raise ClaudeRateLimitError(f"Request rate limit exceeded, retry after {wait_time:.2f} seconds")
        
        # Check token rate limit
        total_tokens = sum(t['tokens'] for t in self.token_usage)
        if total_tokens >= self.rate_limit_tokens_per_minute:
            oldest_token_time = min(t['time'] for t in self.token_usage)
            wait_time = 60 - (current_time - oldest_token_time)
            if wait_time > 0:
                logger.warning(f"Token rate limit reached, waiting {wait_time:.2f} seconds")
                raise ClaudeRateLimitError(f"Token rate limit exceeded, retry after {wait_time:.2f} seconds")
    
    def _make_request_with_backoff(self, payload: Dict[str, Any], max_retries: int = 3) -> Dict[str, Any]:
        """
        Make API request with exponential backoff retry logic.
        
        Args:
            payload: Request payload
            max_retries: Maximum number of retries
            
        Returns:
            API response as dictionary
            
        Raises:
            ClaudeAPIError: If all retries fail
        """
        for attempt in range(max_retries + 1):
            try:
                # Record request time for rate limiting
                current_time = time.time()
                self.request_times.append(current_time)
                
                # Make the request
                response = self.session.post(self.api_url, json=payload, timeout=60)
                
                # Handle different response status codes
                if response.status_code == 200:
                    response_data = response.json()
                    
                    # Record token usage for rate limiting
                    if 'usage' in response_data:
                        total_tokens = response_data['usage'].get('input_tokens', 0) + response_data['usage'].get('output_tokens', 0)
                        self.token_usage.append({
                            'time': current_time,
                            'tokens': total_tokens
                        })
                    
                    return response_data
                
                elif response.status_code == 429:
                    # Rate limit exceeded
                    retry_after = int(response.headers.get('retry-after', 60))
                    if attempt < max_retries:
                        wait_time = min(retry_after, 2 ** attempt)
                        logger.warning(f"Rate limited, waiting {wait_time} seconds before retry {attempt + 1}")
                        time.sleep(wait_time)
                        continue
                    else:
                        raise ClaudeRateLimitError("Rate limit exceeded, max retries reached")
                
                elif response.status_code in [500, 502, 503, 504]:
                    # Server errors - retry with exponential backoff
                    if attempt < max_retries:
                        wait_time = 2 ** attempt
                        logger.warning(f"Server error {response.status_code}, waiting {wait_time} seconds before retry {attempt + 1}")
                        time.sleep(wait_time)
                        continue
                    else:
                        raise ClaudeAPIError(f"Server error {response.status_code}: {response.text}")
                
                elif response.status_code == 401:
                    raise ClaudeAPIError("Authentication failed - check API key")
                
                elif response.status_code == 400:
                    error_data = response.json() if response.headers.get('content-type', '').startswith('application/json') else {}
                    error_message = error_data.get('error', {}).get('message', response.text)
                    raise ClaudeAPIError(f"Bad request: {error_message}")
                
                else:
                    raise ClaudeAPIError(f"Unexpected status code {response.status_code}: {response.text}")
                    
            except requests.exceptions.Timeout:
                if attempt < max_retries:
                    wait_time = 2 ** attempt
                    logger.warning(f"Request timeout, waiting {wait_time} seconds before retry {attempt + 1}")
                    time.sleep(wait_time)
                    continue
                else:
                    raise ClaudeAPIError("Request timeout, max retries reached")
            
            except requests.exceptions.ConnectionError:
                if attempt < max_retries:
                    wait_time = 2 ** attempt
                    logger.warning(f"Connection error, waiting {wait_time} seconds before retry {attempt + 1}")
                    time.sleep(wait_time)
                    continue
                else:
                    raise ClaudeAPIError("Connection error, max retries reached")
            
            except json.JSONDecodeError:
                raise ClaudeAPIError("Invalid JSON response from API")
        
        raise ClaudeAPIError("Max retries exceeded")
    
    def validate_response(self, response: str) -> bool:
        """
        Validate that the response is properly formatted JSON.
        
        Args:
            response: The API response to validate
            
        Returns:
            True if valid, False otherwise
        """
        try:
            data = json.loads(response)
            
            # Check for required fields in analysis response
            required_fields = ['caseId', 'keyFacts']
            for field in required_fields:
                if field not in data:
                    logger.warning(f"Missing required field in response: {field}")
                    return False
            
            return True
            
        except json.JSONDecodeError:
            logger.error("Response is not valid JSON")
            return False
    
    def get_api_status(self) -> Dict[str, Any]:
        """
        Get current API client status and rate limit information.
        
        Returns:
            Dictionary with status information
        """
        current_time = time.time()
        
        # Clean old data
        self.request_times = [t for t in self.request_times if current_time - t < 60]
        self.token_usage = [t for t in self.token_usage if current_time - t['time'] < 60]
        
        return {
            'api_configured': bool(self.api_key),
            'requests_in_last_minute': len(self.request_times),
            'request_rate_limit': self.rate_limit_requests_per_minute,
            'tokens_in_last_minute': sum(t['tokens'] for t in self.token_usage),
            'token_rate_limit': self.rate_limit_tokens_per_minute,
            'model': self.model,
            'max_tokens': self.max_tokens
        }

        
        return json.dumps(mock_response, indent=2)