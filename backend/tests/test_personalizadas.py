# backend/tests/test_personalizadas.py

from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

def test_perguntas_personalizadas():
    # 🔹 Cadastra um aluno (ou ignora se já existir)
    response = client.post("/aluno/cadastro", json={  # ✅ Rota corrigida
        "nome": "Aluno Personalizado",
        "email": "personalizado@example.com",
        "senha": "1234",
        "foto_url": ""
    })
    assert response.status_code in [200, 201, 409]

    # 🔹 Obtém ID do aluno
    aluno_id = 1  # Supondo que seja o ID 1 (ajustável conforme banco)

    # 🔹 Faz a requisição de perguntas personalizadas
    response = client.get(f"/personalizadas/{aluno_id}")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


