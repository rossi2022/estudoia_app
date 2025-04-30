from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

def test_explicacao():
    response = client.post("/explicacao/", json={"pergunta": "O que foi a Revolução Francesa?"})
    assert response.status_code == 200
    data = response.json()
    assert "explicacao" in data
    assert isinstance(data["explicacao"], str)
    assert len(data["explicacao"]) > 0



