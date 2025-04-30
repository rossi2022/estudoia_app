from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from backend.db import get_db
from backend.database.models import Aluno
from backend.schemas import AlunoCreate, AlunoOut

router = APIRouter(
    prefix="/aluno",
    tags=["aluno"]
)

@router.get("/teste", status_code=status.HTTP_200_OK)
def root():
    return {"mensagem": "API EstudoIA está ativa"}

@router.get("/listar", response_model=List[AlunoOut], status_code=status.HTTP_200_OK)
def listar_alunos(db: Session = Depends(get_db)):
    return db.query(Aluno).all()

@router.post("/cadastro", response_model=AlunoOut, status_code=status.HTTP_201_CREATED)
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

@router.get("/{aluno_id}", response_model=AlunoOut, status_code=status.HTTP_200_OK)
def obter_aluno(aluno_id: int, db: Session = Depends(get_db)):
    aluno = db.query(Aluno).filter(Aluno.id == aluno_id).first()
    if not aluno:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Aluno não encontrado.")
    return aluno

@router.put("/{aluno_id}", response_model=AlunoOut, status_code=status.HTTP_200_OK)
def atualizar_aluno(aluno_id: int, dados: AlunoCreate, db: Session = Depends(get_db)):
    aluno = db.query(Aluno).filter(Aluno.id == aluno_id).first()
    if not aluno:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Aluno não encontrado.")
    existente = db.query(Aluno).filter(Aluno.email == dados.email, Aluno.id != aluno_id).first()
    if existente:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email já cadastrado por outro aluno.")
    aluno.nome = dados.nome
    aluno.email = dados.email
    aluno.senha = dados.senha
    aluno.foto_url = dados.foto_url or ""
    db.commit()
    db.refresh(aluno)
    return aluno

@router.delete("/{aluno_id}", status_code=status.HTTP_204_NO_CONTENT)
def deletar_aluno(aluno_id: int, db: Session = Depends(get_db)):
    aluno = db.query(Aluno).filter(Aluno.id == aluno_id).first()
    if not aluno:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Aluno não encontrado.")
    db.delete(aluno)
    db.commit()
    return None









