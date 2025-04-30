import requests
import uuid

def test_mural_conquistas():
    aluno = {
        "nome": "Aluno Mural",
        "email": f"mural_{uuid.uuid4().hex[:6]}@example.com",  # Evita duplicação
        "senha": "1234",
        "nome_pai": "Pai",
        "nome_mae": "Mãe",
        "email_pais": f"pais_{uuid.uuid4().hex[:6]}@example.com"  # Evita duplicação
    }

    # 🔹 Cria o aluno
    criar_aluno = requests.post("http://127.0.0.1:8000/aluno/cadastro", json=aluno)
    print("Resposta do cadastro:", criar_aluno.status_code, criar_aluno.json())

    # 🔹 Pega o ID do aluno (pode vir como 'aluno_id' ou 'id')
    aluno_id = criar_aluno.json().get("aluno_id") or criar_aluno.json().get("id")
    assert aluno_id is not None, "ID do aluno não foi retornado no cadastro"

    # 🔹 Testa o endpoint do mural de conquistas
    resposta = requests.get(f"http://127.0.0.1:8000/conquistas/{aluno_id}")
    print("Resposta do mural:", resposta.status_code, resposta.json())
    assert resposta.status_code == 200



