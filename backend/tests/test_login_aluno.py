# backend/tests/test_login_aluno.py
import requests
import uuid

def test_login_aluno():
    email = f"login_{uuid.uuid4().hex[:8]}@example.com"
    aluno = {
        "nome": "Login Teste",
        "email": email,
        "senha": "1234",
        "nome_pai": "Pai",
        "nome_mae": "Mãe",
        "email_pais": f"pais_{uuid.uuid4().hex[:6]}@example.com"
    }

    # 🔹 Cadastro
    r = requests.post("http://127.0.0.1:8000/aluno/cadastro", json=aluno)
    assert r.status_code in [200, 201]

    # 🔹 Login
    login = {
        "email": email,
        "senha": "1234"
    }
    r = requests.post("http://127.0.0.1:8000/auth/login", json=login)
    print("Login:", r.status_code, r.json())
    assert r.status_code == 200
    data = r.json()
    assert "aluno_id" in data
    assert "mensagem" in data


