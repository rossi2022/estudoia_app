# File: backend/routers/aluno.py
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, Form
from sqlalchemy.orm import Session
from typing import List
from passlib.context import CryptContext
import os
import shutil

from backend.db import get_db
from backend.database.models import Aluno, Medalha
from backend.schemas import AlunoCreate, AlunoOut

router = APIRouter(
    prefix="/aluno",
    tags=["aluno"]
)

# 🔐 Contexto para hash de senha
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# 🔹 Rota de teste
@router.get("/teste", status_code=status.HTTP_200_OK)
def root():
    return {"mensagem": "API EstudoIA está ativa"}

# 🔹 Listar alunos
@router.get("/", response_model=List[AlunoOut], status_code=status.HTTP_200_OK)
@router.get("/listar", response_model=List[AlunoOut], status_code=status.HTTP_200_OK)
def listar_alunos(db: Session = Depends(get_db)):
    return db.query(Aluno).all()

# 🔹 Cadastro com imagem (formData via frontend)
@router.post("/cadastro", response_model=AlunoOut, status_code=status.HTTP_201_CREATED)
async def cadastrar_aluno_upload(
    nome: str = Form(...),
    email: str = Form(...),
    senha: str = Form(...),
    foto: UploadFile = Form(...),
    db: Session = Depends(get_db)
):
    if db.query(Aluno).filter(Aluno.email == email).first():
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email já cadastrado.")
    
    pasta_fotos = "frontend/static/img/alunos"
    os.makedirs(pasta_fotos, exist_ok=True)
    foto_path = os.path.join(pasta_fotos, f"{email}_{foto.filename}")
    with open(foto_path, "wb") as buffer:
        shutil.copyfileobj(foto.file, buffer)

    senha_hash = pwd_context.hash(senha)

    novo = Aluno(
        nome=nome,
        email=email,
        senha=senha_hash,
        foto_url=f"/static/img/alunos/{email}_{foto.filename}"
    )
    db.add(novo)
    db.commit()
    db.refresh(novo)
    return novo

# 🔹 Cadastro via JSON (sem imagem)
@router.post("/", response_model=AlunoOut, status_code=status.HTTP_201_CREATED)
def criar_aluno_json(aluno: AlunoCreate, db: Session = Depends(get_db)):
    if db.query(Aluno).filter(Aluno.email == aluno.email).first():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email já cadastrado.")
    senha_hash = pwd_context.hash(aluno.senha)
    novo = Aluno(
        nome=aluno.nome,
        email=aluno.email,
        senha=senha_hash,
        foto_url=aluno.foto_url or ""
    )
    db.add(novo)
    db.commit()
    db.refresh(novo)
    return novo

# 🔹 Obter aluno por ID
@router.get("/{aluno_id}", response_model=AlunoOut, status_code=status.HTTP_200_OK)
def obter_aluno(aluno_id: int, db: Session = Depends(get_db)):
    aluno = db.query(Aluno).filter(Aluno.id == aluno_id).first()
    if not aluno:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Aluno não encontrado.")
    return aluno

# 🔹 Dashboard: meta, foto, medalhas
@router.get("/{aluno_id}/dashboard", status_code=status.HTTP_200_OK)
def dashboard(aluno_id: int, db: Session = Depends(get_db)):
    aluno = db.query(Aluno).filter(Aluno.id == aluno_id).first()
    if not aluno:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Aluno não encontrado.")

    meta = "Estudar 30 minutos de Matemática por dia."

    medalhas_qs = db.query(Medalha).filter(Medalha.aluno_id == aluno_id).all()
    medalhas = [
        {
            "id": m.id,
            "titulo": m.titulo,
            "descricao": m.descricao,
            "data_conquista": getattr(m, "data_conquista", None) or getattr(m, "data", None)
        }
        for m in medalhas_qs
    ]

    return {
        "nome": aluno.nome,
        "email": aluno.email,
        "foto_url": aluno.foto_url,
        "meta": meta,
        "medalhas": medalhas
    }

# 🔹 Meta de estudo simples
@router.get("/meta/{aluno_id}", status_code=status.HTTP_200_OK)
def obter_meta_estudo(aluno_id: int):
    return {
        "aluno_id": aluno_id,
        "meta": "Estudar 30 minutos por dia de Matemática até sexta-feira."
    }

print("🔐 Rotas de aluno registradas com sucesso.")

