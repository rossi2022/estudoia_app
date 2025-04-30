# backend/test_recompensas.py

import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from backend.main import app
from fastapi.testclient import TestClient

client = TestClient(app)

def test_recompensas_aluno():
    response = client.get("/recompensas/1")  # ✅ rota correta
    assert response.status_code in [200, 404]



