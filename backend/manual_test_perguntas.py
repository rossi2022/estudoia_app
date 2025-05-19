import requests

BASE_URL = "http://127.0.0.1:8000/api"

def pretty_print(resp):
    print(f"Status Code: {resp.status_code}")
    try:
        print(resp.json())
    except ValueError:
        print(resp.text)

# 1) Listar perguntas
print("=== Listar perguntas ===")
resp = requests.get(f"{BASE_URL}/perguntas/")
pretty_print(resp)

# 2) Criar pergunta
print("\n=== Criar pergunta ===")
payload = {
    "materia": "Química",
    "enunciado": "Qual é a fórmula da água?",
    "resposta_correta": "H₂O",
    "dificuldade": "easy"
}
resp = requests.post(f"{BASE_URL}/perguntas/criar", json=payload)
pretty_print(resp)

# 3) Pergunta aleatória
print("\n=== Pergunta aleatória ===")
resp = requests.get(f"{BASE_URL}/perguntas/aleatoria")
pretty_print(resp)

# 4) Filtrar por matéria
print("\n=== Filtrar por matéria=Química ===")
resp = requests.get(f"{BASE_URL}/perguntas/", params={"materia": "Química"})
pretty_print(resp)

# 5) Filtrar por dificuldade=easy
print("\n=== Filtrar por dificuldade=easy ===")
resp = requests.get(f"{BASE_URL}/perguntas/", params={"dificuldade": "easy"})
pretty_print(resp)

# 6) Combinação de filtros
print("\n=== Filtrar por Química & easy ===")
resp = requests.get(f"{BASE_URL}/perguntas/", params={"materia": "Química", "dificuldade": "easy"})
pretty_print(resp)
