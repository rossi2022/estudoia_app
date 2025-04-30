# backend/tests/test_salvar_progresso.py
import requests
import uuid

def test_salvar_progresso():
    # 🔹 Cria um aluno com e-mail único
    email = f"teste_progresso_{uuid.uuid4().hex[:8]}@example.com"
    aluno = {
        "nome": "Aluno Teste Progresso",
        "email": email,
        "senha": "1234",
        "nome_pai": "Pai",
        "nome_mae": "Mãe",
        "email_pais": f"pais_{uuid.uuid4().hex[:6]}@example.com"
    }

    r = requests.post("http://127.0.0.1:8000/aluno/cadastro", json=aluno)
    assert r.status_code in [200, 201]
    aluno_id = r.json().get("id")
    assert aluno_id is not None

    # 🔹 Envia progresso do aluno
    progresso = {
        "aluno_id": aluno_id,
        "materia": "História",
        "acertos": 3,
        "erros": 1
    }
    r = requests.post("http://127.0.0.1:8000/progresso/salvar", json=progresso)
    assert r.status_code in [200, 201]
    assert r.json()["mensagem"].startswith("Progresso registrado")

