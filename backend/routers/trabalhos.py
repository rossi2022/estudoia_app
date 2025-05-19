from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from backend.db import get_db
from backend.database.models import Trabalho, EntregaTrabalho, Professor, Aluno
from backend.schemas import TrabalhoCreate, TrabalhoOut, EntregaCreate, EntregaOut
from backend.utils.security import get_current_user

router = APIRouter(
    prefix="/trabalhos",      # ← prefix adicionado
    tags=["trabalhos"]
)

# 📌 Só professores podem criar trabalhos
@router.post("", response_model=TrabalhoOut, status_code=status.HTTP_201_CREATED)
def criar_trabalho(
    dados: TrabalhoCreate,
    db: Session = Depends(get_db),
    user = Depends(get_current_user)
):
    if user.__class__.__name__ != "Professor" or user.id != dados.professor_id:
        raise HTTPException(403, "Acesso restrito ao próprio professor")
    prof = db.get(Professor, dados.professor_id)
    if not prof:
        raise HTTPException(404, "Professor não encontrado")
    trabalho = Trabalho(**dados.model_dump())
    db.add(trabalho)
    db.commit()
    db.refresh(trabalho)
    return trabalho

# 📌 Fazer entrega de trabalho (aluno)
@router.post("/{trabalho_id}/entregas", response_model=EntregaOut, status_code=status.HTTP_201_CREATED)
def entregar_trabalho(
    trabalho_id: int,
    dados: EntregaCreate,
    db: Session = Depends(get_db),
    user = Depends(get_current_user)
):
    if user.__class__.__name__ != "Aluno" or user.id != dados.aluno_id:
        raise HTTPException(403, "Acesso restrito ao próprio aluno")
    trab = db.get(Trabalho, trabalho_id)
    if not trab:
        raise HTTPException(404, "Trabalho não encontrado")
    entrega = EntregaTrabalho(
        trabalho_id=trabalho_id,
        aluno_id=dados.aluno_id,
        resposta=dados.resposta
    )
    db.add(entrega)
    db.commit()
    db.refresh(entrega)
    return entrega
