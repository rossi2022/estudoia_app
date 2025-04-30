import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

# Caminhos
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FRONTEND_DIR = os.path.abspath(os.path.join(BASE_DIR, "../frontend"))

app = FastAPI(title="EstudoIA App")

# Configuração CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Importação dos routers da API
from backend.routers.auth import router as auth_router
from backend.routers.aluno import router as aluno_router
from backend.routers.progresso import router as progresso_router
from backend.routers.perguntas import router as perguntas_router
# Importe outros routers conforme necessidade
# from backend.routers.prova import router as prova_router
# ...

# Registro de rotas da API com seus prefixes
app.include_router(auth_router, prefix="/auth", tags=["auth"])
app.include_router(aluno_router, prefix="/aluno", tags=["aluno"])
app.include_router(progresso_router, prefix="/progresso", tags=["progresso"])
app.include_router(perguntas_router, prefix="/perguntas", tags=["perguntas"])
# Registre outros routers aqui
# app.include_router(prova_router, prefix="/prova", tags=["prova"])
# ...

# Servir frontend estático (depois das rotas)
app.mount("/", StaticFiles(directory=FRONTEND_DIR, html=True), name="frontend")
































































































