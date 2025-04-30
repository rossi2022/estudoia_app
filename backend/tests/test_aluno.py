import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)  # ✅ Corrigido aqui

def test_criar_aluno():
    response = client.post("/aluno/", json={
        "nome": "Aluno Teste",
        "email": "aluno_teste@example.com",
        "senha": "123456",
        "foto_url": ""
    })
    assert response.status_code in [200, 400]

def test_obter_aluno():
    response = client.get("/aluno/1")
    assert response.status_code in [200, 404]


