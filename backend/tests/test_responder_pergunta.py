# backend/tests/test_responder_pergunta.py
import requests
import uuid

def test_responder_pergunta():
    # 🔹 Cria aluno com e-mail único
    email = f"responder_{uuid.uuid4().hex[:8]}@example.com"
    aluno = {
        "nome": "Aluno Resposta",
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

    # 🔹 Cria pergunta
    pergunta = {
        "materia": "História",
        "enunciado": "Quem descobriu o Brasil?",
        "resposta_correta": "Pedro Álvares Cabral",
        "dificuldade": "facil"
    }
    r = requests.post("http://127.0.0.1:8000/perguntas/criar", json=pergunta)
    assert r.status_code in [200, 201]
    pergunta_id = r.json().get("id")
    assert pergunta_id is not None

    # 🔹 Envia resposta do aluno
    resposta = {
        "aluno_id": aluno_id,
        "pergunta_id": pergunta_id,
        "resposta": "Pedro Álvares Cabral",
        "correta": "sim",
        "materia": "História"
    }
    r = requests.post("http://127.0.0.1:8000/respostas/", json=resposta)  # ✅ Corrigido com barra
    print("Resposta:", r.status_code, r.text)
    assert r.status_code in [200, 201]


