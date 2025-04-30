import requests

BASE_URL = "http://127.0.0.1:8000"

login_data = {
    "email": "joao@email.com",
    "senha": "senha123"
}

print("🔐 Testando login do aluno...")
res = requests.post(f"{BASE_URL}/auth/", json=login_data)

if res.status_code == 200:
    print("✅ Login realizado com sucesso:", res.json())
else:
    print("❌ Falha no login:", res.status_code, res.text)


