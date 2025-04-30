# backend/tests/test_recompensas.py

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

def test_criar_recompensa():
    # Criação de recompensa manual
    response = client.post("/recompensas/criar", json={
        "aluno_id": 1,
        "tipo": "Especial",
        "descricao": "🎯 Teste automático",
        "data": "2025-04-25"
    })
    assert response.status_code == 200
    data = response.json()
    assert data["aluno_id"] == 1
    assert "tipo" in data
    assert "descricao" in data

def test_get_recompensa():
    # Consulta da recompensa gerada (GET)
    response = client.get("/recompensas/1")
    assert response.status_code == 200
    data = response.json()
    assert data["aluno_id"] == 1
    assert "tipo" in data
    assert "descricao" in data





