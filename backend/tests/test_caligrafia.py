# backend/tests/test_caligrafia.py
import uuid
import requests
import pytest
from pathlib import Path
import time

@pytest.fixture
def base_url():
    return "http://localhost:8000"

@pytest.fixture
def aluno_data():
    return {
        "nome": "Aluno Teste Caligrafia",
        "email": f"teste_{uuid.uuid4().hex[:6]}@example.com",
        "senha": "senha123",
        "nome_pai": "Pai Teste",
        "nome_mae": "Mãe Teste",
        "email_pais": f"pais_{uuid.uuid4().hex[:6]}@example.com"
    }

def test_gerar_caligrafia(base_url, aluno_data):
    # 1. Verifica se o servidor está rodando
    try:
        health_check = requests.get(f"{base_url}/docs", timeout=5)
        assert health_check.status_code == 200
    except requests.ConnectionError:
        pytest.fail("Servidor FastAPI não está rodando. Execute 'uvicorn main:app --reload' primeiro.")

    # 2. Cadastra o aluno
    cadastro_response = requests.post(
        f"{base_url}/aluno/cadastro",
        json=aluno_data,
        timeout=10
    )
    
    print("\n=== Dados do Teste ===")
    print("Resposta do cadastro:", cadastro_response.status_code, cadastro_response.json())
    
    assert cadastro_response.status_code == 200, f"Erro no cadastro: {cadastro_response.text}"
    aluno_id = cadastro_response.json().get("id")
    assert aluno_id is not None, "ID do aluno não foi retornado"

    # 3. Gera o PDF de caligrafia
    caligrafia_response = requests.get(
        f"{base_url}/api/caligrafia/{aluno_id}",
        timeout=10
    )
    
    print("Resposta da caligrafia:", caligrafia_response.status_code)
    print("Tipo de conteúdo:", caligrafia_response.headers.get('content-type'))
    
    assert caligrafia_response.status_code == 200, f"Erro ao gerar PDF: {caligrafia_response.text}"
    assert 'application/pdf' in caligrafia_response.headers.get('content-type', ''), "Resposta não é um PDF"

    # 4. Verifica se o arquivo foi criado (opcional)
    pdf_path = Path("backend/arquivos")
    pdf_files = list(pdf_path.glob(f"caligrafia_Aluno_Teste_Caligrafia_*.pdf"))
    assert len(pdf_files) > 0, f"Nenhum PDF foi encontrado em {pdf_path}"

