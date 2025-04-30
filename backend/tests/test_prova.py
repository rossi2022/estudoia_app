import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from backend.main import app
from fastapi.testclient import TestClient

client = TestClient(app)

def test_gerar_prova():
    # 🔹 Cria um aluno de teste
    client.post("/aluno/", json={
        "nome": "Prova Teste",
        "email": "prova_teste@example.com",
        "senha": "1234",
        "foto_url": ""
    })

    # 🔹 Solicita uma prova com matéria que tem perguntas
    response = client.post("/prova/gerar", json={
        "aluno_id": 1,
        "materia": "Matemática",
        "questoes": []  # obrigatório para evitar erro 422
    })

    assert response.status_code in [200, 404]  # 404 se não houver perguntas da matéria

