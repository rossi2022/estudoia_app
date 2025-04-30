from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.db import get_db
from backend.database.models import Prova, QuestaoProva
from pydantic import BaseModel
from typing import List, Optional

router = APIRouter(
    prefix="/prova",
    tags=["Prova"]
)

# 📌 Schema para criação de prova
class ProvaCreate(BaseModel):
    aluno_id: int

class ProvaOut(BaseModel):
    id: int
    aluno_id: int
    nota_final: Optional[float] = None

    class Config:
        orm_mode = True

# 📌 Schema para adicionar questão à prova
class QuestaoCreate(BaseModel):
    prova_id: int
    pergunta_id: int

class QuestaoOut(BaseModel):
    id: int
    prova_id: int
    pergunta_id: int

    class Config:
        orm_mode = True

# ✅ Criar prova
@router.post("/", response_model=ProvaOut)
def criar_prova(prova: ProvaCreate, db: Session = Depends(get_db)):
    nova_prova = Prova(aluno_id=prova.aluno_id)
    db.add(nova_prova)
    db.commit()
    db.refresh(nova_prova)
    return nova_prova

# ✅ Adicionar questão à prova
@router.post("/questoes", response_model=QuestaoOut)
def adicionar_questao(questao: QuestaoCreate, db: Session = Depends(get_db)):
    nova_questao = QuestaoProva(**questao.dict())
    db.add(nova_questao)
    db.commit()
    db.refresh(nova_questao)
    return nova_questao

# ✅ Listar provas (opcional)
@router.get("/", response_model=List[ProvaOut])
def listar_provas(db: Session = Depends(get_db)):
    return db.query(Prova).all()

