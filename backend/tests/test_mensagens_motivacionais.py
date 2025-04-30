# backend/tests/test_mensagens_motivacionais.py

import requests
import uuid

def test_mensagens_motivacionais():
    # 🔹 Criar um e-mail único para evitar duplicidade
    email = f"motiv_{uuid.uuid4().hex[:8]}@example.com"
    aluno = {
        "nome": "Aluno Motivacional",
        "email": email,
        "senha": "1234",
        "nome_pai": "Pai Exemplo",
        "nome_mae": "Mãe Exemplo",
        "email_pais": f"pais_{uuid.uuid4().hex[:6]}@example.com"
    }

    # 🔹 Cadastra o aluno
    r = requests.post("http://127.0.0.1:8000/aluno/cadastro", json=aluno)
    assert r.status_code in [200, 201], f"Erro no cadastro: {r.text}"

    aluno_id = r.json().get("id")
    assert aluno_id is not None, "ID do aluno não retornado"

    # 🔹 Chama a rota de motivação corretamente
    resposta = requests.get(f"http://127.0.0.1:8000/motivacao/{aluno_id}")
    print("Resposta:", resposta.status_code, resposta.text)

    assert resposta.status_code == 200, f"Erro na motivação: {resposta.text}"
    dados = resposta.json()
    assert "mensagem_motivacional" in dados
    assert dados["aluno_id"] == aluno_id







