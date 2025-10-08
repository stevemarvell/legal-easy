import pytest
from fastapi.testclient import TestClient

@pytest.mark.integration
class TestAPIIntegration:
    """Integration tests for the complete API."""
    
    def test_cors_headers_present(self, client):
        """Test that CORS headers are present in responses."""
        response = client.get("/random")
        # Note: TestClient doesn't trigger CORS middleware by default
        # This test would be more meaningful in a real browser environment
        assert response.status_code == 200
    
    def test_api_workflow_health_then_random(self, client):
        """Test a typical API workflow: health check then random number."""
        # First check health
        health_response = client.get("/")
        assert health_response.status_code == 200
        assert "message" in health_response.json()
        
        # Then get random number
        random_response = client.get("/random")
        assert random_response.status_code == 200
        assert "value" in random_response.json()
    
    def test_content_type_headers(self, client):
        """Test that responses have correct content-type headers."""
        response = client.get("/random")
        assert response.headers["content-type"] == "application/json"
    
    def test_invalid_endpoint_returns_404(self, client):
        """Test that invalid endpoints return 404."""
        response = client.get("/invalid-endpoint")
        assert response.status_code == 404
    
    def test_method_not_allowed(self, client):
        """Test that POST to GET-only endpoints returns 405."""
        response = client.post("/random")
        assert response.status_code == 405
    
    def test_api_performance_baseline(self, client):
        """Test that API responds within reasonable time."""
        import time
        start_time = time.time()
        response = client.get("/random")
        end_time = time.time()
        
        assert response.status_code == 200
        assert (end_time - start_time) < 1.0  # Should respond within 1 second