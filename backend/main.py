from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.openapi.utils import get_openapi
from fastapi.security import HTTPBearer

# 📌 Importação das rotas
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
    apostilas,  # ✅ nova rota (SEM parâmetro) deve vir ANTES das rotas com parâmetro
    aluno       # ✅ rota COM parâmetro — DEVE ficar por último
)

app = FastAPI()

# 🔒 Segurança no Swagger
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="EstudoIA API",
        version="1.0.0",
        description="API do sistema EstudoIA",
        routes=app.routes,
    )
    openapi_schema["components"]["securitySchemes"] = {
        "HTTPBearer": {
            "type": "http",
            "scheme": "bearer"
        }
    }
    for path in openapi_schema["paths"].values():
        for method in path.values():
            method["security"] = [{"HTTPBearer": []}]
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi

# ▪️ CORS
origins = ["http://localhost:8000", "http://127.0.0.1:8000"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ▪️ Arquivos estáticos e templates
app.mount("/static", StaticFiles(directory="frontend/static"), name="static")
templates = Jinja2Templates(directory="frontend")

# ▪️ Páginas HTML
@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/professor_login", response_class=HTMLResponse)
async def professor_login(request: Request):
    return templates.TemplateResponse("professor_login.html", {"request": request})

@app.get("/index.html", response_class=HTMLResponse)
async def index_html(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request):
    return templates.TemplateResponse("dashboard.html", {"request": request})

@app.get("/dashboard.html", response_class=HTMLResponse)
async def dashboard_html(request: Request):
    return templates.TemplateResponse("dashboard.html", {"request": request})

@app.get("/quiz", response_class=HTMLResponse)
async def quiz_page(request: Request):
    return templates.TemplateResponse("quiz.html", {"request": request})

@app.get("/quiz.html", response_class=HTMLResponse)
async def quiz_html(request: Request):
    return templates.TemplateResponse("quiz.html", {"request": request})

@app.get("/painel_professor", response_class=HTMLResponse)
async def painel_professor(request: Request):
    return templates.TemplateResponse("painel_professor.html", {"request": request})

@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    return HTMLResponse(content="", status_code=204)

# ▪️ Inclusão das rotas da API
app.include_router(agenda.router, prefix="/api")
app.include_router(agenda_provas.router, prefix="/api")
app.include_router(ai.router, prefix="/api")
app.include_router(auth.router, prefix="/api")
app.include_router(auth_professor.router, prefix="/api")
app.include_router(caligrafia.router, prefix="/api")
app.include_router(conquistas.router, prefix="/api")
app.include_router(escrita.router, prefix="/api")
app.include_router(estudo.router, prefix="/api")
app.include_router(estudos.router, prefix="/api")
app.include_router(estudo_diario.router, prefix="/api")
app.include_router(estudo_guiado.router, prefix="/api")
app.include_router(explicacao.router, prefix="/api")
app.include_router(graficos.router, prefix="/api")
app.include_router(historico_estudos.router, prefix="/api")
app.include_router(leitura_voz.router, prefix="/api")
app.include_router(literatura.router, prefix="/api")
app.include_router(medalhas.router, prefix="/api")
app.include_router(mensagens.router, prefix="/api")
app.include_router(motivacao.router, prefix="/api")
app.include_router(neuroeducacao.router, prefix="/api")
app.include_router(notas.router, prefix="/api")
app.include_router(notas_mensais.router, prefix="/api")
app.include_router(notificacoes.router, prefix="/api")
app.include_router(perguntas.router, prefix="/api")
app.include_router(perguntas_personalizadas.router, prefix="/api")
app.include_router(personalizadas.router, prefix="/api")
app.include_router(planejamento.router, prefix="/api")
app.include_router(professores.router, prefix="/api")
app.include_router(progresso.router, prefix="/api")
app.include_router(prova.router, prefix="/api")
app.include_router(provas_trabalhos.router, prefix="/api")
app.include_router(quiz.router, prefix="/api")
app.include_router(recompensas.router, prefix="/api")
app.include_router(reforco.router, prefix="/api")
app.include_router(relatorio.router, prefix="/api")
app.include_router(relatorio_pdf.router, prefix="/api")
app.include_router(responder.router, prefix="/api")
app.include_router(responder_prova.router, prefix="/api")
app.include_router(respostas.router, prefix="/api")
app.include_router(resumos.router, prefix="/api")
app.include_router(tarefas_estudo.router, prefix="/api")
app.include_router(timeline.router, prefix="/api")
app.include_router(trilha.router, prefix="/api")
app.include_router(trilhas_estudo.router, prefix="/api")
app.include_router(voz.router, prefix="/api")
app.include_router(materias.router, prefix="/api")
app.include_router(apostilas.router, prefix="/api")  # ✅ NOVA ROTA — ANTES DO "aluno"
app.include_router(aluno.router, prefix="/api")       # ✅ ÚLTIMA — pois pode ter /{aluno_id}


























