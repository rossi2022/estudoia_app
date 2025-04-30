import requests

# URL do JSON da especificação OpenAPI
openapi_url = "http://127.0.0.1:8000/openapi.json"

try:
    response = requests.get(openapi_url)
    response.raise_for_status()
    swagger_json = response.json()

    # Lista de todos os paths na especificação
    paths = swagger_json.get("paths", {})

    # Checa se "/respostas/" está presente
    resposta_path = "/respostas/"
    if resposta_path in paths:
        methods = paths[resposta_path]
        # Verifica se POST está disponível
        if "post" in methods:
            print(f"A rota '{resposta_path}' com método POST está disponível na API.")
        else:
            print(f"A rota '{resposta_path}' existe, mas o método POST NÃO está habilitado.")
    else:
        print(f"A rota '{resposta_path}' NÃO aparece na especificação OpenAPI.")
except requests.RequestException as e:
    print(f"Erro ao acessar a especificação OpenAPI: {e}")
except ValueError as e:
    print("Erro ao interpretar a resposta como JSON:", e)

