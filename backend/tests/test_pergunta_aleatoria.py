# backend/tests/test_pergunta_aleatoria.py

import requests

def test_pergunta_aleatoria():
    response = requests.get("http://127.0.0.1:8000/perguntas/aleatoria", params={"materia": "História"})
    print("Resposta:", response.status_code, response.text)
    assert response.status_code == 200
    data = response.json()
    assert "pergunta" in data or "erro" in data


