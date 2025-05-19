from fastapi.testclient import TestClient
from backend.main import app
from backend.db import SessionLocal
from backend.database.models import Professor

client = TestClient(app)

def test_cadastro_trabalho():
    db = SessionLocal()
    email = "prof_trabalho@escola.com"
    existente = db.query(Professor).filter_by(email=email).first()
    if existente:
        db.delete(existente)
        db.commit()

    # 1. Cadastro do professor
    response = client.post(
        "/api/professores/cadastro",
        data={
            "nome": "Professor Trabalho",
            "email": email,
            "senha": "senha123"
        },
        files={"foto": ("foto.jpg", b"fake-image-data", "image/jpeg")}
    )
    assert response.status_code == 201
    professor_id = response.json()["id"]

    # 2. Login do professor
    response = client.post("/api/professores/login", json={
        "email": email,
        "senha": "senha123"
    })
    assert response.status_code == 200
    token = response.json()["token"]

    # 3. Cadastro do trabalho
    response = client.post(
        "/api/trabalhos",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "professor_id": professor_id,
            "titulo": "Trabalho de Teste",
            "tema": "Tema exemplo",
            "prazo_entrega": "2025-06-01"
        }
    )
    assert response.status_code == 201
    assert response.json()["titulo"] == "Trabalho de Teste"
