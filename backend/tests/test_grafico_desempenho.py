import uuid
import requests

BASE = "http://127.0.0.1:8000"

def cria_aluno():
    email = f"graf_{uuid.uuid4().hex[:6]}@exemplo.com"
    payload = {
        "nome": "Teste Gráfico",
        "email": email,
        "senha": "1234",
        "nome_pai": "Pai Teste",
        "nome_mae": "Mãe Teste",
        "email_pais": f"pais_{uuid.uuid4().hex[:6]}@exemplo.com"
    }
    r = requests.post(f"{BASE}/aluno/cadastro", json=payload)
    assert r.status_code in (200, 201), f"Cadastro falhou: {r.text}"
    return r.json()["id"]

def registra_progresso(aluno_id, materia, acertos, erros):
    payload = {
        "aluno_id": aluno_id,
        "materia": materia,
        "acertos": acertos,
        "erros": erros
    }
    r = requests.post(f"{BASE}/progresso/salvar", json=payload)
    assert r.status_code in (200, 201), f"Salvar progresso falhou: {r.text}"

def test_grafico_desempenho():
    # 1) Cria aluno
    aluno_id = cria_aluno()

    # 2) Registra diferentes desempenhos
    registra_progresso(aluno_id, "Matemática", 5, 2)
    registra_progresso(aluno_id, "História",    3, 1)
    registra_progresso(aluno_id, "História",    4, 0)

    # 3) Pede dados do gráfico
    r = requests.get(f"{BASE}/graficos/desempenho/{aluno_id}")
    assert r.status_code == 200, f"GET gráfico falhou: {r.text}"
    data = r.json()

    # 4) Valida estrutura do JSON retornado
    assert "Matemática" in data, "Matemática não retornada"
    assert "História"    in data, "História não retornada"

    # 5) Cada matéria deve ser lista de objetos com data, acertos e erros
    for materia, entradas in data.items():
        assert isinstance(entradas, list), f"{materia} não é lista"
        for item in entradas:
            assert "data"    in item, f"Falta data em {materia}"
            assert "acertos" in item, f"Falta acertos em {materia}"
            assert "erros"   in item, f"Falta erros em {materia}"
