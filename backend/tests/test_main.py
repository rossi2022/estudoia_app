# backend/tests/test_main.py

from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

def test_root():
    response = client.get("/aluno/")
    assert response.status_code == 200 or response.status_code == 404

def test_cadastro_aluno():
    response = client.post("/aluno/cadastro", json={  # ✅ Rota corrigida
        "nome": "Teste Aluno",
        "email": "teste_aluno@example.com",
        "senha": "1234",
        "nome_pai": "Pai Teste",
        "nome_mae": "Mãe Teste",
        "email_pais": "pais@example.com"
    })
    assert response.status_code in [200, 201, 409]

