import importlib


def test_read_root(client):
    response = client.get("/")
    assert response.status_code == 200
    assert "message" in response.json()


def test_health_check(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_documented_backend_entrypoint_imports_app():
    backend_main = importlib.import_module("backend.main")
    api_main = importlib.import_module("api.main")
    assert backend_main.app is api_main.app
