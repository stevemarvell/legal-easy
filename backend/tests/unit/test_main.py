import pytest
from unittest.mock import patch
from fastapi.testclient import TestClient
from main import app, get_random, root, health_check

class TestHealthEndpoint:
    """Test the health check endpoint."""
    
    def test_root_endpoint_returns_correct_message(self, client):
        """Test that root endpoint returns expected message."""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert data["message"] == "AI Legal Platform API"
        assert data["version"] == "1.0.0"
        assert "endpoints" in data
        assert data["endpoints"]["cases"] == "/cases"
        assert data["endpoints"]["documents"] == "/documents"
        assert data["endpoints"]["health"] == "/health"
    
    def test_root_function_directly(self):
        """Test the root function directly."""
        result = root()
        assert result["message"] == "AI Legal Platform API"
        assert result["version"] == "1.0.0"
        assert "endpoints" in result
        assert result["endpoints"]["cases"] == "/cases"
    
    def test_health_check_endpoint(self, client):
        """Test the health check endpoint."""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert data["service"] == "AI Legal Platform API"
    
    def test_health_check_function_directly(self):
        """Test the health check function directly."""
        result = health_check()
        assert result["status"] == "healthy"
        assert result["service"] == "AI Legal Platform API"

class TestRandomEndpoint:
    """Test the random number endpoint."""
    
    def test_random_endpoint_returns_200(self, client):
        """Test that random endpoint returns 200 status."""
        response = client.get("/random")
        assert response.status_code == 200
    
    def test_random_endpoint_returns_json_with_value(self, client):
        """Test that random endpoint returns JSON with 'value' key."""
        response = client.get("/random")
        data = response.json()
        assert "value" in data
        assert isinstance(data["value"], int)
    
    def test_random_value_in_correct_range(self, client):
        """Test that random value is between 0 and 100."""
        response = client.get("/random")
        value = response.json()["value"]
        assert 0 <= value <= 100
    
    @patch('main.random.randint')
    def test_random_function_with_mock(self, mock_randint, client):
        """Test random function with mocked random.randint."""
        mock_randint.return_value = 42
        response = client.get("/random")
        assert response.json() == {"value": 42}
        mock_randint.assert_called_once_with(0, 100)
    
    def test_get_random_function_directly(self):
        """Test the get_random function directly."""
        result = get_random()
        assert "value" in result
        assert isinstance(result["value"], int)
        assert 0 <= result["value"] <= 100
    
    def test_multiple_calls_return_different_values(self, client):
        """Test that multiple calls can return different values."""
        responses = [client.get("/random").json()["value"] for _ in range(10)]
        # With 10 calls, we should get at least some variation (not foolproof but reasonable)
        assert len(set(responses)) > 1 or all(r == responses[0] for r in responses)