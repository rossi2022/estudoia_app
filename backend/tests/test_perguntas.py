import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from backend.main import app
from fastapi.testclient import TestClient

client = TestClient(app)

def test_progresso_aluno():
    response = client.get("/progresso/1")
    assert response.status_code in [200, 404]


