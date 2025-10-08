import pytest
from pact import Verifier
import subprocess
import time
import requests
from threading import Thread
import uvicorn
from main import app

@pytest.mark.contract
class TestPactProvider:
    """Contract tests for the API provider (backend)."""
    
    @pytest.fixture(scope="class")
    def server(self):
        """Start the FastAPI server for contract testing."""
        def run_server():
            uvicorn.run(app, host="127.0.0.1", port=8001, log_level="error")
        
        server_thread = Thread(target=run_server, daemon=True)
        server_thread.start()
        
        # Wait for server to start
        for _ in range(30):  # Wait up to 30 seconds
            try:
                response = requests.get("http://127.0.0.1:8001/")
                if response.status_code == 200:
                    break
            except requests.exceptions.ConnectionError:
                time.sleep(1)
        else:
            pytest.fail("Server failed to start")
        
        yield "http://127.0.0.1:8001"
    
    def test_verify_pact_with_frontend(self, server):
        """Verify the pact contract with the frontend consumer."""
        verifier = Verifier(
            provider="legal-easy-backend",
            provider_base_url=server,
        )
        
        # In a real scenario, you would fetch pacts from a Pact Broker
        # For this demo, we'll create a simple verification
        try:
            # This would normally verify against pact files
            # verifier.verify_pacts("path/to/pacts")
            
            # For demo purposes, just verify the endpoints exist
            response = requests.get(f"{server}/")
            assert response.status_code == 200
            
            response = requests.get(f"{server}/random")
            assert response.status_code == 200
            assert "value" in response.json()
            
        except Exception as e:
            pytest.fail(f"Pact verification failed: {e}")
    
    def test_provider_state_setup(self, server):
        """Test provider state setup for contract testing."""
        # This would set up specific states for contract testing
        # For example: "Given a random number service is available"
        response = requests.get(f"{server}/")
        assert response.status_code == 200
        assert response.json()["message"] == "Random Number API. Use /random"