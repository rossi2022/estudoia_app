# File: backend/tests/test_app_client.py

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from backend.main import app
from backend.db import get_db
from backend.database.models import Base

# URL de teste: banco SQLite local (arquivo) ou memória
TEST_DATABASE_URL = "sqlite:///./test_estudoia.db"
engine_test = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine_test
)

@pytest.fixture(scope="module")
def client():
    # Cria as tabelas no banco de testes
    Base.metadata.create_all(bind=engine_test)

    # Override da dependência get_db para usar o banco de teste
    def override_get_db():
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as c:
        yield c

    # Cleanup: remove tabelas após os testes
    Base.metadata.drop_all(bind=engine_test)


def test_registration_and_login_and_dashboard(client):
    # 1) Cadastro de aluno
    cadastro_payload = {
        "nome": "TC",
        "email": "tc@test.com",
        "senha": "1234",
        "foto_url": ""
    }
    resp = client.post(
        "/api/aluno/cadastro",
        json=cadastro_payload
    )
    assert resp.status_code in (201, 409)

    # 2) Login
    login_payload = {"email": "tc@test.com", "senha": "1234"}
    resp = client.post(
        "/api/auth/login",
        json=login_payload
    )
    assert resp.status_code == 200
    data = resp.json()
    assert "token" in data and "aluno_id" in data
    token = data["token"]
    aluno_id = data["aluno_id"]

    # 3) Dashboard protegido
    headers = {"Authorization": f"Bearer {token}"}
    resp = client.get(f"/api/aluno/{aluno_id}/dashboard", headers=headers)
    assert resp.status_code == 200
    body = resp.json()
    assert body.get("nome") == "TC"
