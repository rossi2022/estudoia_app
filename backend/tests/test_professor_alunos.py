from fastapi.testclient import TestClient
from backend.main import app
from backend.db import SessionLocal
from backend.database.models import Professor, Aluno
from passlib.context import CryptContext

client = TestClient(app)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def test_listar_alunos_com_token():
    db = SessionLocal()

    # 🧪 Cria professor
    email_prof = "listar_alunos@escola.com"
    senha = "senha123"

    existente = db.query(Professor).filter_by(email=email_prof).first()
    if existente:
        db.delete(existente)
        db.commit()

    professor = Professor(
        nome="Professor Listagem",
        email=email_prof,
        senha=pwd_context.hash(senha),
        foto_url=""
    )
    db.add(professor)
    db.commit()

    # 🔐 Login para obter token
    resp = client.post("/api/professores/login", json={
        "email": email_prof,
        "senha": senha
    })
    assert resp.status_code == 200
    token = resp.json()["token"]

    # ➕ Cria aluno de teste
    aluno = Aluno(
        nome="Aluno Teste",
        email="aluno_teste@teste.com",
        senha=pwd_context.hash("123456"),
    )
    db.add(aluno)
    db.commit()

    # 📥 Requisição para listar alunos com token
    response = client.get(
        "/api/professores/alunos",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200
    alunos = response.json()
    assert any(a["email"] == "aluno_teste@teste.com" for a in alunos)
