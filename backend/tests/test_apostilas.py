# tests/test_apostilas.py

from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

def test_listar_apostilas():
    response = client.get("/api/apostilas/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

