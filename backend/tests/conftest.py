import pytest
from fastapi.testclient import TestClient
from main import app

@pytest.fixture
def client():
    """Create a test client for the FastAPI app."""
    return TestClient(app)

@pytest.fixture
def sample_random_response():
    """Sample response for random endpoint."""
    return {"value": 42}

@pytest.fixture
def health_response():
    """Sample response for health endpoint."""
    return {"message": "Random Number API. Use /random"}