import uuid
import requests

def test_mensagem_motivacional():
    # 🔹 Cria aluno com e-mail único
    aluno = {
        "nome": "Aluno Motivacional",
        "email": f"motiv_{uuid.uuid4().hex[:6]}@example.com",
        "senha": "1234",
        "nome_pai": "Pai Motivacional",
        "nome_mae": "Mãe Motivacional",
        "email_pais": f"paismotiv_{uuid.uuid4().hex[:6]}@example.com"
    }

    criar = requests.post("http://127.0.0.1:8000/aluno/cadastro", json=aluno)
    print("Cadastro:", criar.status_code, criar.json())
    assert criar.status_code in [200, 201]

    aluno_id = criar.json().get("id")
    assert aluno_id is not None

    # 🔹 Envia desempenho do aluno
    desempenho = {
        "aluno_id": aluno_id,
        "materia": "História",
        "acertos": 3,
        "erros": 1
    }

    resposta = requests.post("http://127.0.0.1:8000/progresso/salvar", json=desempenho)
    print("Desempenho:", resposta.status_code, resposta.json())
    assert resposta.status_code in [200, 201]

    # 🔹 Consulta mensagem motivacional
    motivacao = requests.get(f"http://127.0.0.1:8000/motivacao/{aluno_id}")
    print("Motivação:", motivacao.status_code, motivacao.json())
    assert motivacao.status_code == 200
    assert "mensagem" in motivacao.json()


