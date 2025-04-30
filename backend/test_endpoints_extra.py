# backend/test_endpoints_extra.py

import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from backend.main import app
from fastapi.testclient import TestClient

client = TestClient(app)

def test_get_perguntas():
    response = client.get("/perguntas/")
    assert response.status_code == 200

def test_get_aluno_por_id():
    response = client.get("/aluno/1")
    assert response.status_code in [200, 404]

def test_get_progresso_do_aluno():
    response = client.get("/progresso/1")
    assert response.status_code in [200, 404]

def test_get_relatorio():
    response = client.get("/relatorio/1")
    assert response.status_code in [200, 404]

def test_get_recompensas():
    response = client.get("/recompensas/1")
    assert response.status_code in [200, 404]

def test_get_medalhas():
    response = client.get("/recompensas/1/medalhas")
    assert response.status_code in [200, 404]




