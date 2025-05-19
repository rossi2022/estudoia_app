# File: backend/tests/conftest.py

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from backend.main import app
from backend.db import get_db
from backend.database.models import Base

# Banco SQLite em arquivo temporário
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
    # Cria todas as tabelas
    Base.metadata.create_all(bind=engine_test)

    # Override do get_db para usar o banco de teste
    def override_get_db():
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()
    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as c:
        yield c

    # Limpa tudo depois
    Base.metadata.drop_all(bind=engine_test)



