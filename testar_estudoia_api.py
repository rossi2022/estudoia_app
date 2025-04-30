
import requests

BASE_URL = "http://127.0.0.1:8000"

# 1. Criar novo aluno
print("==> Criando novo aluno")
aluno_data = {
    "nome": "João Silva",
    "email": "joao@email.com",
    "senha": "senha123"
}
res = requests.post(f"{BASE_URL}/aluno/", json=aluno_data)
print("Resposta:", res.status_code, res.json())

# 2. Fazer login
print("\n==> Fazendo login")
login_data = {
    "email": "joao@email.com",
    "senha": "senha123"
}
res = requests.post(f"{BASE_URL}/login", json=login_data)
print("Resposta:", res.status_code, res.json())

# Usar ID 1 como exemplo (ajuste conforme necessário)
aluno_id = 1

# 3. Buscar aluno por ID
print("\n==> Buscando aluno por ID")
res = requests.get(f"{BASE_URL}/aluno/{aluno_id}")
print("Resposta:", res.status_code, res.json())

# 4. Ver medalhas do aluno
print("\n==> Ver medalhas do aluno")
res = requests.get(f"{BASE_URL}/medalhas/{aluno_id}")
print("Resposta:", res.status_code, res.json())

# 5. Ver progresso do aluno
print("\n==> Ver progresso do aluno")
res = requests.get(f"{BASE_URL}/progresso/{aluno_id}")
print("Resposta:", res.status_code, res.json())

# 6. Ver reforço sugerido
print("\n==> Ver reforço sugerido")
res = requests.get(f"{BASE_URL}/recompensas/reforco/{aluno_id}")
print("Resposta:", res.status_code, res.json())
