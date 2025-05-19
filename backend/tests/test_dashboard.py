# File: tests/test_dashboard.py

import pytest
from fastapi.testclient import TestClient
from backend.main import app
from backend.db import SessionLocal
from backend.database.models import Aluno

client = TestClient(app)

@pytest.fixture(scope="module")
def aluno_com_foto():
    db = SessionLocal()
    aluno = Aluno(
        nome="FotoTeste",
        email="foto@teste.com",
        senha="senhasegura123",
        foto_url="/static/img/alunos/foto_teste.jpg"
    )
    db.add(aluno)
    db.commit()
    db.refresh(aluno)
    yield aluno
    db.delete(aluno)
    db.commit()
    db.close()

def test_dashboard_retorna_foto_url(aluno_com_foto):
    aluno_id = aluno_com_foto.id
    response = client.get(f"/api/aluno/{aluno_id}/dashboard")
    assert response.status_code == 200
    data = response.json()
    assert data["nome"] == "FotoTeste"
    assert data["email"] == "foto@teste.com"
    assert "foto_url" in data
    assert data["foto_url"] == "/static/img/alunos/foto_teste.jpg"
