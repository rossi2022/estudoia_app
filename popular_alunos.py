import requests

API_URL = "http://127.0.0.1:8000/aluno/cadastro"
headers = {"Content-Type": "application/json"}

alunos = [
    {"nome": "Alice Santos", "email": "alice.santos@example.com", "senha": "senha123", "foto_url": ""},
    {"nome": "Bruno Costa", "email": "bruno.costa@example.com", "senha": "senha123", "foto_url": ""},
    {"nome": "Carla Mendes", "email": "carla.mendes@example.com", "senha": "senha123", "foto_url": ""},
    {"nome": "Diego Lima", "email": "diego.lima@example.com", "senha": "senha123", "foto_url": ""},
    {"nome": "Eduarda Silva", "email": "eduarda.silva@example.com", "senha": "senha123", "foto_url": ""},
    {"nome": "Fábio Rocha", "email": "fabio.rocha@example.com", "senha": "senha123", "foto_url": ""},
    {"nome": "Gabriela Souza", "email": "gabriela.souza@example.com", "senha": "senha123", "foto_url": ""},
    {"nome": "Henrique Martins", "email": "henrique.martins@example.com", "senha": "senha123", "foto_url": ""},
]

for aluno in alunos:
    response = requests.post(API_URL, json=aluno, headers=headers)
    if response.status_code == 201:
        print(f"✅ Aluno cadastrado: {aluno['nome']}")
    elif response.status_code == 409:
        print(f"⚠️ Já existia: {aluno['nome']} ({aluno['email']})")
    else:
        print(f"❌ Erro ao cadastrar {aluno['nome']}: {response.status_code} {response.text}")






