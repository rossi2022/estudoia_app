import uuid
import requests

def test_prova_aluno():
    # 🔹 Cria aluno com e-mail único
    aluno = {
        "nome": "Aluno Prova",
        "email": f"prova_{uuid.uuid4().hex[:6]}@example.com",  # E-mail único
        "senha": "1234",
        "nome_pai": "Pai Prova",
        "nome_mae": "Mãe Prova",
        "email_pais": f"paisprova_{uuid.uuid4().hex[:6]}@example.com"  # Também único
    }
    r = requests.post("http://127.0.0.1:8000/aluno/cadastro", json=aluno)
    print("Cadastro:", r.status_code, r.json())
    assert r.status_code in [200, 201]
    
    aluno_id = r.json().get("id")
    assert aluno_id is not None

    # 🔹 Gera prova (adaptar para seu endpoint real se precisar)
    response = requests.get(f"http://127.0.0.1:8000/prova/gerar/{aluno_id}")
    print("Prova:", response.status_code, response.text)
    assert response.status_code == 200


