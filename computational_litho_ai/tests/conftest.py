import pytest
from fastapi.testclient import TestClient
from backend.main import app  # Adjust if your app is in a different location

@pytest.fixture(scope="module")
def client():
    with TestClient(app) as c:
        yield c

