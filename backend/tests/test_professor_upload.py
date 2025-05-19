import os
from fastapi.testclient import TestClient
from backend.main import app
from backend.db import SessionLocal
from backend.database.models import Professor

client = TestClient(app)

def test_cadastro_professor_com_imagem():
    db = SessionLocal()
    email = "professor_teste@escola.com"

    # Remove professor se já existir
    existente = db.query(Professor).filter_by(email=email).first()
    if existente:
        db.delete(existente)
        db.commit()

    # Caminho seguro da imagem
    test_dir = os.path.dirname(__file__)
    imagem_teste = os.path.join(test_dir, "teste_professor.jpg")

    # Cria imagem JPEG válida (com cabeçalho real)
    with open(imagem_teste, "wb") as f:
        f.write(
            b"\xFF\xD8\xFF\xE0"  # JPEG header
            + b"\x00" * 1024     # Dados de preenchimento
            + b"\xFF\xD9"        # JPEG footer
        )

    # Faz o POST simulando o upload
    with open(imagem_teste, "rb") as img:
        response = client.post(
            "/api/professores/cadastro",
            files={"foto": ("teste_professor.jpg", img, "image/jpeg")},
            data={
                "nome": "Professor Teste",
                "email": email,
                "senha": "senha123"
            }
        )

    # Remove imagem após o teste
    if os.path.exists(imagem_teste):
        os.remove(imagem_teste)

    # Validação da resposta
    assert response.status_code == 201, f"Erro: {response.text}"
    data = response.json()
    assert data["nome"] == "Professor Teste"
    assert data["email"] == email
    assert "foto_url" in data
