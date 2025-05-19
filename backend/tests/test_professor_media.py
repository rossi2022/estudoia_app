from fastapi.testclient import TestClient
from backend.main import app
from backend.db import SessionLocal
from backend.database.models import Professor, NotaMensal
from passlib.context import CryptContext

client = TestClient(app)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def test_media_desempenho():
    db = SessionLocal()

    # 🧪 Cria professor
    email = "media_prof@escola.com"
    senha = "senha123"

    existente = db.query(Professor).filter_by(email=email).first()
    if existente:
        db.delete(existente)
        db.commit()

    professor = Professor(
        nome="Professor Média",
        email=email,
        senha=pwd_context.hash(senha),
        foto_url=""
    )
    db.add(professor)
    db.commit()

    # 🔐 Login
    resp = client.post("/api/professores/login", json={
        "email": email,
        "senha": senha
    })
    assert resp.status_code == 200
    token = resp.json()["token"]

    # ➕ Cria notas de exemplo
    nota1 = NotaMensal(aluno_id=1, materia="Matemática", nota=8.0, mes="Maio", ano=2025)
    nota2 = NotaMensal(aluno_id=1, materia="Matemática", nota=6.0, mes="Abril", ano=2025)
    nota3 = NotaMensal(aluno_id=1, materia="História", nota=9.0, mes="Março", ano=2025)

    db.add_all([nota1, nota2, nota3])
    db.commit()

    # 📥 Consulta a média
    response = client.get(
        "/api/professores/media-desempenho",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200
    dados = response.json()
    assert "Matemática" in dados
    assert dados["Matemática"] == 7.0
    assert dados["História"] == 9.0
