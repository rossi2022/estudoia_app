# File: backend/routers/auth.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from backend.db import get_db
from backend.database.models import Aluno
from backend.schemas import AlunoCreate, AlunoOut, LoginData, LoginResponse

router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)

# 🔹 CADASTRO DE ALUNO
@router.post(
    "/",
    response_model=AlunoOut,
    status_code=status.HTTP_201_CREATED
)
def cadastrar_aluno(aluno: AlunoCreate, db: Session = Depends(get_db)):
    if db.query(Aluno).filter(Aluno.email == aluno.email).first():
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email já cadastrado.")
    novo = Aluno(
        nome=aluno.nome,
        email=aluno.email,
        senha=aluno.senha,
        foto_url=aluno.foto_url or ""
    )
    db.add(novo)
    db.commit()
    db.refresh(novo)
    return novo

# 🔹 LOGIN DE ALUNO
@router.post(
    "/login",
    response_model=LoginResponse,
    status_code=status.HTTP_200_OK
)
def login_aluno(creds: LoginData, db: Session = Depends(get_db)):
    aluno = db.query(Aluno).filter(
        Aluno.email == creds.email,
        Aluno.senha == creds.senha
    ).first()
    if not aluno:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciais inválidas."
        )
    # Gere um token de verdade aqui; usamos um dummy por enquanto
    token = "fake-jwt-token"
    return LoginResponse(
        message="Login bem-sucedido",
        aluno_id=aluno.id,
        nome=aluno.nome,
        token=token
    )






























