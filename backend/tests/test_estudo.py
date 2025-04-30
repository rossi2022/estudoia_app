# backend/tests/test_estudo.py

from fastapi.testclient import TestClient
from backend.main import app
from backend.db import SessionLocal
from backend.utils.test_setup import garantir_aluno_teste

client = TestClient(app)

def test_registrar_estudo_diario():
    db = SessionLocal()
    aluno = garantir_aluno_teste(db)
    db.close()

    response = client.post("/estudo/registrar", json={"aluno_id": aluno.id})
    
    assert response.status_code == 200
    data = response.json()
    
    assert "mensagem" in data
    assert data["mensagem"] == "Estudo diário registrado com sucesso"
    assert "total_dias" in data
    assert isinstance(data["total_dias"], int)
    assert data["total_dias"] >= 1

