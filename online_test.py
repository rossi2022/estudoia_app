# online_test.py
import os
import pytest
import requests

BASE = "https://estudoia-app.fly.dev"

@pytest.fixture(scope="session")
def professor_token():
    email = os.getenv("TEST_PROF_EMAIL")
    senha = os.getenv("TEST_PROF_PASS")
    assert email and senha, "Defina as vars TEST_PROF_EMAIL e TEST_PROF_PASS antes de rodar os testes"
    r = requests.post(
        f"{BASE}/api/professores/login",
        json={"email": email, "senha": senha}
    )
    assert r.status_code == 200, f"Login falhou: {r.text}"
    return r.json()["token"]

@pytest.fixture(scope="session")
def auth_headers(professor_token):
    return {"Authorization": f"Bearer {professor_token}"}

def test_criar_pergunta(auth_headers):
    payload = {
        "materia": "Matemática",
        "pergunta": "Quanto é 3+5?",
        "resposta_correta": "8",
        "dificuldade": "fácil"
    }
    r = requests.post(f"{BASE}/api/perguntas/", json=payload, headers=auth_headers)
    assert r.status_code == 201, f"Falha ao criar pergunta: {r.text}"

def test_listar_perguntas(auth_headers):
    r = requests.get(f"{BASE}/api/perguntas/", headers=auth_headers)
    assert r.status_code == 200, f"Erro ao listar perguntas: {r.text}"
    assert isinstance(r.json(), list)

def test_get_pergunta_aleatoria(auth_headers):
    r = requests.get(f"{BASE}/api/perguntas/aleatoria", headers=auth_headers)
    assert r.status_code == 200, f"Erro na pergunta aleatória: {r.text}"
    q = r.json()
    assert "id" in q and "pergunta" in q
