# backend/tests/test_trilha_estudo.py

from fastapi.testclient import TestClient
from backend.main import app
from backend.db import SessionLocal
from backend.database.models import Aluno

client = TestClient(app)

def garantir_aluno_trilha():
    db = SessionLocal()
    aluno = db.query(Aluno).filter(Aluno.email == "trilha@example.com").first()
    if not aluno:
        novo = Aluno(nome="Aluno Trilha", email="trilha@example.com", senha="1234", foto_url="")
        db.add(novo)
        db.commit()
        db.refresh(novo)
        aluno_id = novo.id
    else:
        aluno_id = aluno.id
    db.close()
    return aluno_id

def test_trilha_estudo():
    aluno_id = garantir_aluno_trilha()
    response = client.get(f"/trilhas-estudo/{aluno_id}")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0
    assert "titulo" in data[0]
    assert "habilidade" in data[0]


