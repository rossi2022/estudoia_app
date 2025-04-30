# backend/tests/test_trilha.py

import sys, os
import pytest
from fastapi.testclient import TestClient

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from backend.main import app
from backend.db import SessionLocal
from backend.database.models import TrilhaAprendizado

client = TestClient(app)

# 🔸 Função auxiliar para limpar as trilhas após cada teste (boa prática)
def limpar_trilhas():
    db = SessionLocal()
    db.query(TrilhaAprendizado).delete()
    db.commit()
    db.close()

@pytest.fixture(autouse=True)
def run_around_tests():
    limpar_trilhas()
    yield
    limpar_trilhas()

# 🔹 1. Teste: Criar uma nova trilha
def test_criar_trilha():
    response = client.post("/trilha/", json={
        "aluno_id": 1,
        "titulo": "Melhorar Redação",
        "descricao": "Praticar escrita com foco no ENEM",
        "habilidade": "Escrita argumentativa"
    })
    assert response.status_code == 200
    data = response.json()
    assert data["titulo"] == "Melhorar Redação"
    assert data["status"] == "pendente"

# 🔹 2. Teste: Listar trilhas de um aluno
def test_listar_trilhas():
    client.post("/trilha/", json={
        "aluno_id": 1,
        "titulo": "Matemática",
        "descricao": "Resolver problemas",
        "habilidade": "Raciocínio lógico"
    })
    client.post("/trilha/", json={
        "aluno_id": 1,
        "titulo": "Português",
        "descricao": "Interpretar textos",
        "habilidade": "Compreensão textual"
    })

    response = client.get("/trilha/1")
    assert response.status_code == 200
    trilhas = response.json()
    assert len(trilhas) == 2
    assert trilhas[0]["aluno_id"] == 1

# 🔹 3. Teste: Marcar uma trilha como concluída
def test_concluir_trilha():
    criar = client.post("/trilha/", json={
        "aluno_id": 1,
        "titulo": "História",
        "descricao": "Estudar Brasil Império",
        "habilidade": "Contexto histórico"
    })
    trilha_id = criar.json()["id"]

    response = client.put(f"/trilha/{trilha_id}/concluir")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "concluída"

