# backend/routers/resumos.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.db import get_db
from backend.database.models import Resumo  # agora importando corretamente
from backend import schemas
from datetime import datetime

router = APIRouter(
    prefix="/resumos",
    tags=["Resumos"]
)

# 🔹 Rota para criar um resumo
@router.post("/", response_model=schemas.ResumoOut)
def criar_resumo(resumo: schemas.ResumoRequest, db: Session = Depends(get_db)):
    novo_resumo = Resumo(
        aluno_id=resumo.aluno_id,
        conteudo=resumo.texto,
        data=datetime.utcnow()  # ✅ garante que a data seja preenchida
    )
    db.add(novo_resumo)
    db.commit()
    db.refresh(novo_resumo)
    return novo_resumo

# 🔹 Rota para listar resumos por aluno
@router.get("/{aluno_id}", response_model=list[schemas.ResumoOut])
def listar_resumos(aluno_id: int, db: Session = Depends(get_db)):
    resumos = db.query(Resumo).filter(Resumo.aluno_id == aluno_id).all()
    return resumos





