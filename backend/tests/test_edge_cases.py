# backend/tests/test_edge_cases.py

from fastapi.testclient import TestClient
from backend.main import app
from backend.db import SessionLocal
from backend.utils.test_setup import garantir_aluno_teste

client = TestClient(app)


def test_cadastro_com_email_duplicado():
    payload = {
        "nome": "Aluno Repetido",
        "email": "duplicado@example.com",
        "senha": "senha123",
        "foto_url": ""
    }

    response1 = client.post("/aluno/cadastro", json=payload)
    assert response1.status_code in [200, 201, 409]

    response2 = client.post("/aluno/cadastro", json=payload)
    assert response2.status_code == 409


def test_explicacao_com_pergunta_vazia():
    response = client.post("/explicacao/", json={"pergunta": ""})
    assert response.status_code == 200
    data = response.json()
    assert "explicacao" in data



def test_envio_audio_com_tipo_incorreto():
    fake_audio = b"This is not a real audio file"
    response = client.post(
        "/voz/avaliar",
        files={"arquivo_audio": ("fake.txt", fake_audio, "text/plain")}
    )
    assert response.status_code in [400, 422, 500]


def test_cadastro_com_nome_ausente():
    response = client.post("/aluno/cadastro", json={
        "email": "semnome@example.com",
        "senha": "senha123",
        "foto_url": ""
    })
    assert response.status_code == 422


def test_perguntas_personalizadas_com_id_invalido():
    response = client.get("/personalizadas/999999")
    assert response.status_code == 404


