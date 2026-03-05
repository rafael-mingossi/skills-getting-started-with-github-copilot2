import pytest
from fastapi.testclient import TestClient
from src.app import app


@pytest.fixture
def client():
    """
    Fixture that provides a TestClient for the FastAPI app.
    Uses the shared in-memory activities database.
    """
    return TestClient(app)
