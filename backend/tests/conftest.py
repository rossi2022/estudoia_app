import sys
import os
import pytest
from fastapi.testclient import TestClient

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from backend.main import app
from backend.db import Base, engine

# Garante que as tabelas sejam criadas antes dos testes
@pytest.fixture(scope="session", autouse=True)
def setup_database():
    Base.metadata.create_all(bind=engine)

@pytest.fixture(scope="module")
def client():
    with TestClient(app) as c:  # ✅ Corrigido aqui
        yield c



