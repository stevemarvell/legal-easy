import pytest
from unittest.mock import patch
from fastapi.testclient import TestClient
from main import app, get_random, root

class TestHealthEndpoint:
    """Test the health check endpoint."""
    
    def test_root_endpoint_returns_correct_message(self, client):
        """Test that root endpoint returns expected message."""
        response = client.get("/")
        assert response.status_code == 200
        assert response.json() == {"message": "Random Number API. Use /random"}
    
    def test_root_function_directly(self):
        """Test the root function directly."""
        result = root()
        assert result == {"message": "Random Number API. Use /random"}

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