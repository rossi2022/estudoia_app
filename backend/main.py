# File: backend/main.py

import os
from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.openapi.utils import get_openapi

# —————————————————————————————————————————————————————————————
# Banco de dados e Base declarativa (via backend/db.py)
# —————————————————————————————————————————————————————————————
from backend.db import engine, Base, get_db

# Garante que todas as tabelas serão criadas antes de qualquer request
Base.metadata.create_all(bind=engine)

# —————————————————————————————————————————————————————————————
# Importa todos os routers
# —————————————————————————————————————————————————————————————
from backend.routers import (
    agenda,
    agenda_provas,
    ai,
    auth,
    auth_professor,
    caligrafia,
    conquistas,
    escrita,
    estudo,
    estudos,
    estudo_diario,
    estudo_guiado,
    explicacao,
    graficos,
    historico_estudos,
    leitura_voz,
    literatura,
    medalhas,
    mensagens,
    motivacao,
    neuroeducacao,
    notas,
    notas_mensais,
    notificacoes,
    perguntas,
    perguntas_personalizadas,
    personalizadas,
    planejamento,
    professores,
    progresso,
    prova,
    provas_trabalhos,
    quiz,
    recompensas,
    reforco,
    relatorio,
    relatorio_pdf,
    responder,
    responder_prova,
    respostas,
    resumos,
    tarefas_estudo,
    timeline,
    trilha,
    trilhas_estudo,
    voz,
    materias,
    apostilas,
    aluno,
    trabalhos
)

all_routers = [
    agenda.router,
    agenda_provas.router,
    ai.router,
    auth.router,
    auth_professor.router,
    caligrafia.router,
    conquistas.router,
    escrita.router,
    estudo.router,
    estudos.router,
    estudo_diario.router,
    estudo_guiado.router,
    explicacao.router,
    graficos.router,
    historico_estudos.router,
    leitura_voz.router,
    literatura.router,
    medalhas.router,
    mensagens.router,
    motivacao.router,
    neuroeducacao.router,
    notas.router,
    notas_mensais.router,
    notificacoes.router,
    perguntas.router,
    perguntas_personalizadas.router,
    personalizadas.router,
    planejamento.router,
    professores.router,
    progresso.router,
    prova.router,
    provas_trabalhos.router,
    quiz.router,
    recompensas.router,
    reforco.router,
    relatorio.router,
    relatorio_pdf.router,
    responder.router,
    responder_prova.router,
    respostas.router,
    resumos.router,
    tarefas_estudo.router,
    timeline.router,
    trilha.router,
    trilhas_estudo.router,
    voz.router,
    materias.router,
    apostilas.router,
    aluno.router,
    trabalhos.router,
]

# —————————————————————————————————————————————————————————————
# Configura FastAPI com docs sob /api
# —————————————————————————————————————————————————————————————
app = FastAPI(
    title="EstudoIA API",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json"
)


# Custom OpenAPI para exigir Bearer em todas as rotas de API
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title=app.title,
        version=app.version,
        description="API do sistema EstudoIA",
        routes=app.routes,
    )
    openapi_schema["components"]["securitySchemes"] = {
        "HTTPBearer": {"type": "http", "scheme": "bearer"}
    }
    for path in openapi_schema["paths"].values():
        for method in path.values():
            method["security"] = [{"HTTPBearer": []}]
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi

# —————————————————————————————————————————————————————————————
# CORS (frontend local)
# —————————————————————————————————————————————————————————————
origins = ["http://localhost:8000", "http://127.0.0.1:8000"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# —————————————————————————————————————————————————————————————
# Monta arquivos estáticos e templates Jinja
# —————————————————————————————————————————————————————————————
BASE_DIR = Path(__file__).resolve().parent.parent
static_path = BASE_DIR / "frontend" / "static"
templates_path = BASE_DIR / "frontend" / "templates"

app.mount("/static", StaticFiles(directory=str(static_path)), name="static")
templates = Jinja2Templates(directory=str(templates_path))


# —————————————————————————————————————————————————————————————
# Páginas HTML do frontend
# —————————————————————————————————————————————————————————————
@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/index.html", response_class=HTMLResponse)
async def index_html(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/professor_login", response_class=HTMLResponse)
async def professor_login(request: Request):
    return templates.TemplateResponse("professor_login.html", {"request": request})

@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request):
    return templates.TemplateResponse("dashboard.html", {"request": request})

@app.get("/quiz", response_class=HTMLResponse)
async def quiz_page(request: Request):
    return templates.TemplateResponse("quiz.html", {"request": request})

@app.get("/painel_professor", response_class=HTMLResponse)
async def painel_professor(request: Request):
    return templates.TemplateResponse("painel_professor.html", {"request": request})

@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    return HTMLResponse(status_code=204)


# —————————————————————————————————————————————————————————————
# Monta **todos** os routers sob /api **e** sem prefixo
# —————————————————————————————————————————————————————————————
for router in all_routers:
    app.include_router(router, prefix="/api")
    app.include_router(router, prefix="")

















