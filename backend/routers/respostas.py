from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from backend.db import get_db
from backend.database.models import RespostaAluno
from pydantic import BaseModel

router = APIRouter(
    prefix="/respostas",
    tags=["Respostas"]
)

# 🔹 Schema Pydantic para entrada de resposta
class RespostaAlunoSchema(BaseModel):
    aluno_id: int
    pergunta_id: int
    resposta: str
    correta: str
    materia: str

    class Config:
        from_attributes = True  # ✅ compatível com Pydantic v2

# ✅ Endpoint POST para criar uma resposta
@router.post("/", response_model=RespostaAlunoSchema, status_code=201)
def criar_resposta(resposta: RespostaAlunoSchema, db: Session = Depends(get_db)):
    try:
        nova_resposta = RespostaAluno(**resposta.dict())
        db.add(nova_resposta)
        db.commit()
        db.refresh(nova_resposta)
        return nova_resposta
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Erro ao criar resposta: {str(e)}")

# ✅ Endpoint GET para listar respostas
@router.get("/", response_model=List[RespostaAlunoSchema])
def listar_respostas(db: Session = Depends(get_db)):
    return db.query(RespostaAluno).all()













