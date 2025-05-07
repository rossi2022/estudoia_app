# File: backend/routers/notas.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from backend.db import get_db
from backend.database.models import NotaMensal, Aluno
from backend.schemas import NotaMensalCreate, NotaMensalOut

router = APIRouter(
    prefix="/notas",
    tags=["notas"]
)

# 🔹 Criar nova nota
@router.post("/", response_model=NotaMensalOut, status_code=status.HTTP_201_CREATED)
def criar_nota(nota: NotaMensalCreate, db: Session = Depends(get_db)):
    aluno = db.query(Aluno).filter(Aluno.id == nota.aluno_id).first()
    if not aluno:
        raise HTTPException(status_code=404, detail="Aluno não encontrado")

    nova_nota = NotaMensal(**nota.dict())
    db.add(nova_nota)
    db.commit()
    db.refresh(nova_nota)
    return nova_nota

# 🔹 Listar todas as notas de um aluno
@router.get("/{aluno_id}", response_model=List[NotaMensalOut])
def listar_notas(aluno_id: int, db: Session = Depends(get_db)):
    aluno = db.query(Aluno).filter(Aluno.id == aluno_id).first()
    if not aluno:
        raise HTTPException(status_code=404, detail="Aluno não encontrado")

    return db.query(NotaMensal).filter(NotaMensal.aluno_id == aluno_id).all()






