import pytest
import importlib

httpx = importlib.util.find_spec("httpx")
if httpx is None:
    pytest.skip("httpx is required for API tests", allow_module_level=True)

from fastapi.testclient import TestClient
from api.main import app

@pytest.fixture(scope="module")
def client():
    with TestClient(app) as c:
        yield c

