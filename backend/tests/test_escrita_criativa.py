# backend/tests/test_escrita_criativa.py

import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from backend.main import app
from fastapi.testclient import TestClient
from backend.db import SessionLocal
from backend.database.models import Aluno, EscritaCriativa

client = TestClient(app)

def setup_module(module):
    """Garante que um aluno de teste esteja presente no banco."""
    db = SessionLocal()
    aluno = db.query(Aluno).filter(Aluno.email == "escrita@example.com").first()
    if not aluno:
        aluno = Aluno(nome="Aluno Escritor", email="escrita@example.com", senha="1234")
        db.add(aluno)
        db.commit()
        db.refresh(aluno)
    db.close()

def test_criar_escrita_criativa():
    """Testa a criação de uma nova escrita criativa."""
    db = SessionLocal()
    aluno = db.query(Aluno).filter(Aluno.email == "escrita@example.com").first()
    db.close()

    response = client.post("/escrita/", json={
        "aluno_id": aluno.id,
        "tema": "O mundo em 2050",
        "texto": "Em 2050, o mundo terá avançado tecnologicamente..."
    })
    assert response.status_code in [200, 201]
    data = response.json()
    assert "feedback" in data or "id" in data

def test_listar_escritas_do_aluno():
    """Testa a listagem de escritas criativas de um aluno."""
    db = SessionLocal()
    aluno = db.query(Aluno).filter(Aluno.email == "escrita@example.com").first()
    db.close()

    response = client.get(f"/escrita/{aluno.id}")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
