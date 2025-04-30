from fastapi.testclient import TestClient
from backend.main import app
from backend.db import SessionLocal
from backend.utils.test_setup import garantir_aluno_teste

client = TestClient(app)

def test_estudo_diario():
    db = SessionLocal()
    aluno = garantir_aluno_teste(db)
    db.close()

    response = client.get(f"/estudo/diario/{aluno.id}")
    
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) <= 10  # Deve retornar até 10 perguntas
    for pergunta in data:
        assert "materia" in pergunta
        assert "pergunta" in pergunta
