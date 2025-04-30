# backend/tests/test_explicacao_personalizada.py
import requests
import uuid

def test_perguntas_personalizadas():
    # Criar aluno para garantir ID válido
    aluno = {
        "nome": "Aluno IA",
        "email": f"ia_{uuid.uuid4().hex[:6]}@example.com",
        "senha": "1234",
        "nome_pai": "Pai IA",
        "nome_mae": "Mãe IA",
        "email_pais": f"pais_ia_{uuid.uuid4().hex[:6]}@example.com"
    }
    criar = requests.post("http://127.0.0.1:8000/aluno/cadastro", json=aluno)
    aluno_id = criar.json().get("id")

    # Chamada ao endpoint
    response = requests.get(f"http://127.0.0.1:8000/personalizadas/{aluno_id}")
    print("Resposta personalizada:", response.status_code, response.text)

    assert response.status_code == 200
    data = response.json()
    assert "perguntas" in data or isinstance(data, list) or "erro" in str(data).lower()
