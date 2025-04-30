# backend/tests/test_grafico_aluno.py
import requests
import uuid

def test_grafico_desempenho():
    # 🔹 Cria aluno com e-mail único
    email_unico = f"grafico_{uuid.uuid4().hex[:8]}@example.com"
    aluno = {
        "nome": "Aluno Grafico",
        "email": email_unico,
        "senha": "1234",
        "nome_pai": "Pai",
        "nome_mae": "Mãe",
        "email_pais": f"pais_{uuid.uuid4().hex[:6]}@example.com"
    }

    r = requests.post("http://127.0.0.1:8000/aluno/cadastro", json=aluno)
    print("Cadastro:", r.status_code, r.json())
    assert r.status_code in [200, 201]

    aluno_id = r.json().get("id")
    assert aluno_id is not None

    # 🔹 Cria perguntas no banco para associar com respostas
    perguntas = [
        {"materia": "História", "enunciado": "Quando foi a Independência do Brasil?", "resposta_correta": "1822", "dificuldade": "media"}
    ]
    pergunta_ids = []
    for p in perguntas:
        resp = requests.post("http://127.0.0.1:8000/perguntas/criar", json=p)
        assert resp.status_code in [200, 201], f"Erro ao criar pergunta: {resp.text}"
        pergunta_ids.append(resp.json().get("id"))

    # 🔹 Envia resposta
    resposta = {
        "aluno_id": aluno_id,
        "pergunta_id": pergunta_ids[0],
        "resposta": "1822",
        "correta": "sim",
        "materia": "História"
    }
    r = requests.post("http://127.0.0.1:8000/respostas", json=resposta)
    print("Resposta:", r.status_code, r.text)
    assert r.status_code in [200, 201]

    # 🔹 Requisição do gráfico de desempenho
    response = requests.get(f"http://127.0.0.1:8000/graficos/{aluno_id}")
    print("Gráfico:", response.status_code, response.json())
    assert response.status_code == 200
    assert "medias" in response.json()


