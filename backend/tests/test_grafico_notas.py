# backend/tests/test_grafico_notas.py
import requests
import uuid

def test_grafico_notas():
    # 🔹 Cria aluno único
    email = f"grafico_notas_{uuid.uuid4().hex[:8]}@example.com"
    aluno = {
        "nome": "Aluno Notas",
        "email": email,
        "senha": "1234",
        "nome_pai": "Pai",
        "nome_mae": "Mãe",
        "email_pais": f"pais_{uuid.uuid4().hex[:6]}@example.com"
    }

    r = requests.post("http://127.0.0.1:8000/aluno/cadastro", json=aluno)
    assert r.status_code in [200, 201]
    aluno_id = r.json().get("id")
    assert aluno_id

    # 🔹 Registra nota mensal
    nota = {
        "aluno_id": aluno_id,
        "materia": "Matemática",
        "nota": 8.5,
        "mes": "Abril"
    }
    r = requests.post("http://127.0.0.1:8000/notas", json=nota)
    assert r.status_code in [200, 201]

    # 🔹 Consulta gráfico de progresso
    response = requests.get(f"http://127.0.0.1:8000/progresso/{aluno_id}")
    print("Gráfico Notas:", response.status_code, response.json())
    assert response.status_code == 200
    assert isinstance(response.json(), dict)
    assert "Matemática" in response.json()

