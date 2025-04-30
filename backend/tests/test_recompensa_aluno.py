import uuid
import requests

def test_recompensa_aluno():
    # 🔹 Cria aluno com e-mail único
    aluno = {
        "nome": "Aluno Recompensa",
        "email": f"recompensa_{uuid.uuid4().hex[:6]}@example.com",  # E-mail dinâmico
        "senha": "1234",
        "nome_pai": "Pai Recompensa",
        "nome_mae": "Mãe Recompensa",
        "email_pais": f"paisrecompensa_{uuid.uuid4().hex[:6]}@example.com"
    }

    criar = requests.post("http://127.0.0.1:8000/aluno/cadastro", json=aluno)
    print("Cadastro:", criar.status_code, criar.json())
    assert criar.status_code in [200, 201], f"Erro no cadastro: {criar.text}"

    aluno_id = criar.json().get("id")
    assert aluno_id is not None, "ID do aluno não retornado"

    # 🔹 Adiciona nota mensal para gerar recompensa
    nota = {
        "aluno_id": aluno_id,
        "materia": "Matemática",
        "nota": 9.0,
        "mes": "Abril"
    }
    nota_resp = requests.post("http://127.0.0.1:8000/notas/", json=nota)  # ✅ barra final corrigida
    try:
        print("Nota:", nota_resp.status_code, nota_resp.json())
    except Exception:
        print("Erro na resposta de nota:", nota_resp.status_code, nota_resp.text)

    assert nota_resp.status_code in [200, 201], f"Erro ao registrar nota: {nota_resp.text}"

    # 🔹 Consulta recompensas (agora com nota!)
    resposta = requests.get(f"http://127.0.0.1:8000/recompensas/{aluno_id}")
    print("Recompensas:", resposta.status_code, resposta.json())
    assert resposta.status_code == 200, f"Falha ao buscar recompensa: {resposta.text}"





