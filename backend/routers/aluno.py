# File: backend/routers/aluno.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from passlib.context import CryptContext  # 🔐 Import para hash de senha

from backend.db import get_db
from backend.database.models import Aluno
from backend.schemas import AlunoCreate, AlunoOut

router = APIRouter(
    prefix="/aluno",
    tags=["aluno"]
)

# 🔐 Inicializa contexto de senha
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# 🔹 Teste rápido da API
@router.get("/teste", status_code=status.HTTP_200_OK)
def root():
    return {"mensagem": "API EstudoIA está ativa"}

# 🔹 Listar todos os alunos
@router.get("/", response_model=List[AlunoOut], status_code=status.HTTP_200_OK)
@router.get("/listar", response_model=List[AlunoOut], status_code=status.HTTP_200_OK)
def listar_alunos(db: Session = Depends(get_db)):
    return db.query(Aluno).all()

# 🔹 Cadastrar aluno via rota /cadastro
@router.post("/cadastro", response_model=AlunoOut, status_code=status.HTTP_201_CREATED)
def cadastrar_aluno(aluno: AlunoCreate, db: Session = Depends(get_db)):
    if db.query(Aluno).filter(Aluno.email == aluno.email).first():
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email já cadastrado.")
    
    senha_hash = pwd_context.hash(aluno.senha)  # 🔐 Criptografa senha

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

# 🔹 Cadastrar aluno via POST /
@router.post("/", response_model=AlunoOut, status_code=status.HTTP_201_CREATED)
def criar_aluno(aluno: AlunoCreate, db: Session = Depends(get_db)):
    if db.query(Aluno).filter(Aluno.email == aluno.email).first():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email já cadastrado.")
    
    senha_hash = pwd_context.hash(aluno.senha)  # 🔐 Criptografa senha

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

# 🔹 Meta de estudo simulada para o aluno
@router.get("/meta/{aluno_id}")
def obter_meta_estudo(aluno_id: int):
    return {
        "aluno_id": aluno_id,
        "meta": "Estudar 30 minutos por dia de Matemática até sexta-feira."
    }

print("🔐 Rota /auth/login registrada com sucesso.")

