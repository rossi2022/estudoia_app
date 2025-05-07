# File: backend/routers/resumos.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from backend.db import get_db
from backend.database.models import Resumo, Aluno
from pydantic import BaseModel, ConfigDict
from datetime import datetime

router = APIRouter(
    prefix="/resumos",
    tags=["Resumos"]
)

# 🔹 Esquemas
class ResumoCreate(BaseModel):
    aluno_id: int
    conteudo: str

class ResumoOut(BaseModel):
    id: int
    aluno_id: int
    conteudo: str
    data: datetime

    model_config = ConfigDict(from_attributes=True)

# 🔸 Criar resumo
@router.post("/", response_model=ResumoOut, status_code=status.HTTP_201_CREATED)
def criar_resumo(resumo: ResumoCreate, db: Session = Depends(get_db)):
    aluno = db.query(Aluno).filter(Aluno.id == resumo.aluno_id).first()
    if not aluno:
        raise HTTPException(status_code=404, detail="Aluno não encontrado")

    novo_resumo = Resumo(aluno_id=resumo.aluno_id, conteudo=resumo.conteudo)
    db.add(novo_resumo)
    db.commit()
    db.refresh(novo_resumo)
    return novo_resumo

# 🔸 Listar todos os resumos de um aluno
@router.get("/listar/{aluno_id}", response_model=list[ResumoOut])
def listar_resumos(aluno_id: int, db: Session = Depends(get_db)):
    resumos = db.query(Resumo).filter(Resumo.aluno_id == aluno_id).order_by(Resumo.data.desc()).all()
    return resumos

# 🔸 Último resumo diário
@router.get("/resumo/{aluno_id}", response_model=str)
def resumo_diario(aluno_id: int, db: Session = Depends(get_db)):
    resumo = (
        db.query(Resumo)
        .filter(Resumo.aluno_id == aluno_id)
        .order_by(Resumo.data.desc())
        .first()
    )
    if not resumo:
        raise HTTPException(status_code=404, detail="Nenhum resumo encontrado")
    return resumo.conteudo





