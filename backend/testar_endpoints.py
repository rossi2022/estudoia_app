# backend/testar_endpoints.py

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from backend.main import app
from fastapi.testclient import TestClient

client = TestClient(app)

rotas_para_testar = [
    "/", "/docs", "/aluno/", "/auth/login", "/progresso/progresso/1",
    "/pergunta/perguntas", "/prova/prova/gerar", "/relatorio/relatorio/1",
    "/recompensas/recompensas/1", "/explicacao/", "/graficos/graficos/1",
    "/literatura/literatura/trecho", "/medalhas/medalhas/medalhas/1",
    "/notas/notas_mensais/1", "/notas_mensais/notas_mensais/1",
    "/notificacoes/notificacoes/lembrete", "/notificacoes/notificacoes/motivacional",
    "/relatorio_pdf/relatorio/1", "/reforco/reforco/1", "/responder/responder",
    "/respostas/responder", "/trilha/trilhas-estudo/1", "/trilhas-estudo/trilhas-estudo/1",
    "/neuroeducacao/neuroeducacao/1", "/personalizadas/1"
]

for rota in rotas_para_testar:
    metodo = "get"
    if rota.endswith("/responder"):
        metodo = "post"
    response = getattr(client, metodo)(rota)
    status = response.status_code
    print(f"{rota} -> {status} {'✅' if status in [200, 404, 422] else '❌'}")

