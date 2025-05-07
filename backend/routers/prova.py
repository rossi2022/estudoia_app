# File: backend/routers/prova.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime

from backend.db import get_db
from backend.database.models import Prova, QuestaoProva
from pydantic import BaseModel

router = APIRouter(
    prefix="/prova",
    tags=["Prova"]
)

# 📌 Schema para criação de prova
class ProvaCreate(BaseModel):
    aluno_id: int
    nome: Optional[str] = "Prova Automática"
    data_prova: Optional[datetime] = None
    conteudo: Optional[str] = None

class ProvaOut(BaseModel):
    id: int
    aluno_id: int
    nome: Optional[str]
    data_prova: Optional[datetime]
    conteudo: Optional[str]
    nota_final: Optional[float] = None

    class Config:
        from_attributes = True  # compatível com Pydantic v2

# 📌 Schema para adicionar questão à prova
class QuestaoCreate(BaseModel):
    prova_id: int
    pergunta_id: int

class QuestaoOut(BaseModel):
    id: int
    prova_id: int
    pergunta_id: int

    class Config:
        from_attributes = True

# ✅ Criar prova
@router.post("/", response_model=ProvaOut)
def criar_prova(prova: ProvaCreate, db: Session = Depends(get_db)):
    nova_prova = Prova(
        aluno_id=prova.aluno_id,
        nome=prova.nome or "Prova Automática",
        data_prova=prova.data_prova or datetime.utcnow(),
        conteudo=prova.conteudo or "Conteúdo gerado automaticamente"
    )
    db.add(nova_prova)
    db.commit()
    db.refresh(nova_prova)
    return nova_prova

# ✅ Adicionar questão à prova
@router.post("/questoes", response_model=QuestaoOut)
def adicionar_questao(questao: QuestaoCreate, db: Session = Depends(get_db)):
    nova_questao = QuestaoProva(**questao.dict())
    db.add(nova_questao)















