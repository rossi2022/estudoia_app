# File: backend/tests/test_app_routes.py

import pytest

# Usa a fixture 'client' definida em test_app_client.py

def test_meta_estudo(client):
    # Cria um aluno e testa rota de meta sem autenticação
    cadastro_payload = {
        "nome": "MetaTester",
        "email": "meta@test.com",
        "senha": "meta123",
        "foto_url": ""
    }
    resp = client.post("/api/aluno/cadastro", json=cadastro_payload)
    assert resp.status_code in (201, 409)

    # Login para obter aluno_id
    login_resp = client.post(
        "/api/auth/login",
        json={"email": "meta@test.com", "senha": "meta123"}
    )
    assert login_resp.status_code == 200
    aluno_id = login_resp.json()["aluno_id"]

    # Rota de meta de estudo
    resp = client.get(f"/api/aluno/meta/{aluno_id}")
    assert resp.status_code == 200
    data = resp.json()
    assert data.get("aluno_id") == aluno_id
    assert isinstance(data.get("meta"), str)


def test_listar_perguntas(client):
    # Consulta lista de perguntas (rota pública)
    resp = client.get("/api/perguntas/")
    assert resp.status_code == 200
    assert isinstance(resp.json(), list)


def test_criar_pergunta(client):
    # Cria uma nova pergunta
    payload = {
        "materia": "Física",
        "pergunta": "Qual é a fórmula de gravitação universal?",
        "resposta_correta": "F = G m1 m2 / r^2",
        "dificuldade": "medium"
    }
    resp = client.post("/api/perguntas/", json=payload)
    assert resp.status_code in (200, 201)
    data = resp.json()
    assert data.get("materia") == payload["materia"]
    assert data.get("pergunta") == payload["pergunta"]


def test_get_recompensas(client):
    # Cria e autentica um aluno para testar recompensas
    cadastro_payload = {
        "nome": "RewardTester",
        "email": "reward@test.com",
        "senha": "reward123",
        "foto_url": ""
    }
    client.post("/api/aluno/cadastro", json=cadastro_payload)
    login_resp = client.post(
        "/api/auth/login",
        json={"email": "reward@test.com", "senha": "reward123"}
    )
    assert login_resp.status_code == 200
    token = login_resp.json()["token"]
    aluno_id = login_resp.json()["aluno_id"]

    headers = {"Authorization": f"Bearer {token}"}
    resp = client.get(f"/api/recompensas/{aluno_id}", headers=headers)
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, (dict, list))
    if isinstance(data, dict):
        assert data.get("aluno_id") == aluno_id

