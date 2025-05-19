# File: tests/test_user_flow.py

from fastapi.testclient import TestClient
from backend.main import app
from backend.db import SessionLocal
from backend.database.models import Aluno

client = TestClient(app)

def test_dashboard_retorna_foto_url():
    db = SessionLocal()
    aluno = Aluno(
        nome="FotoFlow",
        email="fotoflow@test.com",
        senha="senhaflow123",
        foto_url="/static/img/alunos/foto_flow.jpg"
    )
    db.add(aluno)
    db.commit()
    db.refresh(aluno)

    response = client.get(f"/api/aluno/{aluno.id}/dashboard")
    assert response.status_code == 200
    data = response.json()
    assert data["nome"] == "FotoFlow"
    assert data["email"] == "fotoflow@test.com"
    assert data["foto_url"] == "/static/img/alunos/foto_flow.jpg"

    db.delete(aluno)
    db.commit()
    db.close()

