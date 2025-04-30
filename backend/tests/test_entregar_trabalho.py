# backend/tests/test_entregar_trabalho.py

import sys
import os
import pytest
from fastapi.testclient import TestClient

# 📌 Ajuste do caminho para importações
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from backend.main import app

client = TestClient(app)

@pytest.fixture
def trabalho_exemplo():
    """Fixture para criar um trabalho de exemplo"""
    # Você pode usar um ID real que exista no seu banco, ou já criar um no teste.
    return {
        "trabalho_id": 1,  # 👈 ajuste se precisar
        "aluno_id": 1,     # 👈 ajuste se precisar
        "resposta": "Esta é a resposta de teste para o trabalho."
    }

def test_entregar_trabalho(trabalho_exemplo):
    resposta = {
        "aluno_id": trabalho_exemplo["aluno_id"],
        "resposta": trabalho_exemplo["resposta"]
    }
    response = client.post(f"/estudos/trabalhos/{trabalho_exemplo['trabalho_id']}/entregar", json=resposta)

    assert response.status_code == 200, f"Erro inesperado: {response.text}"
    resultado = response.json()

    assert "mensagem" in resultado
    assert "entrega_id" in resultado
    assert "data_entrega" in resultado
    assert resultado["mensagem"] == "Trabalho entregue e registrado com sucesso!"
