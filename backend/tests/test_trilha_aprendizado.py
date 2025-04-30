import requests

def test_trilha_aprendizado():
    aluno = {
        "nome": "Aluno Trilha",
        "email": "trilha@example.com",
        "senha": "1234",
        "nome_pai": "Pai",
        "nome_mae": "Mãe",
        "email_pais": "paistrilha@example.com"
    }
    r = requests.post("http://127.0.0.1:8000/aluno/cadastro", json=aluno)
    assert r.status_code in [200, 201]
    aluno_id = r.json().get("aluno_id")

    trilha = {
        "aluno_id": aluno_id,
        "titulo": "Metas de Redação",
        "descricao": "Dominar estrutura do texto dissertativo",
        "habilidade": "Escrita"
    }

    resposta = requests.post("http://127.0.0.1:8000/trilha", json=trilha)
    assert resposta.status_code == 200
    assert "titulo" in resposta.json()
