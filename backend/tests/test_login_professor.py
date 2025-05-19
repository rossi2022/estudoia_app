from fastapi.testclient import TestClient
from backend.main import app
from backend.db import SessionLocal
from backend.database.models import Professor
from passlib.context import CryptContext

client = TestClient(app)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def test_login_professor():
    db = SessionLocal()
    email = "professor_teste_login@escola.com"
    senha = "senha123"

    # 🔁 Remove se já existir
    existente = db.query(Professor).filter_by(email=email).first()
    if existente:
        db.delete(existente)
        db.commit()

    # ➕ Cria professor manualmente
    novo = Professor(
        nome="Professor Login",
        email=email,
        senha=pwd_context.hash(senha),
        foto_url="/static/img/professores/login_teste.jpg"
    )
    db.add(novo)
    db.commit()

    # 🔐 Faz login
    response = client.post("/api/professores/login", json={
        "email": email,
        "senha": senha
    })

    assert response.status_code == 200
    data = response.json()
    assert "token" in data
    assert data["nome"] == "Professor Login"
