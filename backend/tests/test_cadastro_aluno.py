import requests

def test_cadastro_aluno():
    url = "http://127.0.0.1:8000/aluno/cadastro"
    aluno = {
        "nome": "João da Silva",
        "email": "joao@example.com",
        "senha": "1234",
        "nome_pai": "Carlos Silva",
        "nome_mae": "Ana Silva",
        "email_pais": "pais@example.com"
    }

    response = requests.post(url, json=aluno)
    if response.status_code == 409:
        assert True  # aluno já existe, OK
    else:
        assert response.status_code in [200, 201]

