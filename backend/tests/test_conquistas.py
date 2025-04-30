# backend/tests/test_conquistas.py

from fastapi.testclient import TestClient
from backend.main import app
from backend.db import SessionLocal
from backend.database.models import Aluno, Conquista
from datetime import date

client = TestClient(app)

def criar_aluno_com_conquista():
    db = SessionLocal()

    # Garante e-mail único
    email = "conquista_teste@example.com"
    aluno = db.query(Aluno).filter(Aluno.email == email).first()
    if not aluno:
        aluno = Aluno(nome="Aluno Conquista", email=email, senha="1234", foto_url="")
        db.add(aluno)
        db.commit()
        db.refresh(aluno)

    # Garante que a conquista não seja duplicada
    conquista_existente = db.query(Conquista).filter(Conquista.aluno_id == aluno.id).first()
    if not conquista_existente:
        conquista = Conquista(
            aluno_id=aluno.id,
            titulo="Primeira Vitória",
            descricao="Completou a primeira meta!",
            data_conquista=date.today()
        )
        db.add(conquista)
        db.commit()

    db.close()
    return aluno.id

def test_mural_conquistas():
    aluno_id = criar_aluno_com_conquista()

    # Testa a rota principal
    response = client.get(f"/conquistas/{aluno_id}")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0
    assert "titulo" in data[0]
    assert "descricao" in data[0]
    assert "data_conquista" in data[0]

    # Testa também a rota /mural/{aluno_id}
    response_mural = client.get(f"/conquistas/mural/{aluno_id}")
    assert response_mural.status_code == 200
    mural = response_mural.json()
    assert isinstance(mural, list)
    assert len(mural) > 0







