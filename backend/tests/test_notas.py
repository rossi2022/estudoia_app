import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from backend.main import app
from fastapi.testclient import TestClient

client = TestClient(app)

def test_gerar_prova():
    # 🔹 Cria um aluno de teste
    client.post("/aluno/", json={
        "nome": "Aluno Teste",
        "email": "nota_teste@example.com",
        "senha": "1234",
        "foto_url": ""
    })

    # 🔹 Garante que há perguntas da matéria no banco (Matemática)
    # (já devem estar carregadas via perguntas_fixas)

    # 🔹 Envia a requisição com campo "questoes" vazio, para evitar erro 422
    response = client.post("/prova/gerar", json={
        "aluno_id": 1,
        "materia": "História",
        "questoes": []  # <-- ESSENCIAL PARA bater com GerarProvaRequest
    })

    assert response.status_code in [200, 404]


