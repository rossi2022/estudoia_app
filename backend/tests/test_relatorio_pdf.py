import requests

def test_relatorio_pdf():
    aluno_id = 1
    response = requests.get(f"http://127.0.0.1:8000/relatorio/{aluno_id}")

    assert response.status_code == 200
    assert response.headers["content-type"] == "application/pdf"
