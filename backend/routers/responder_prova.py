# File: backend/routers/responder_prova.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.db import get_db
from backend.database.models import Prova, RespostaProva
from pydantic import BaseModel
from typing import List

router = APIRouter(
    prefix="/responder-prova",
    tags=["Responder Prova"]
)

# 🔹 Modelo de entrada
class RespostaProvaIn(BaseModel):
    prova_id: int
    pergunta_id: int
    resposta_aluno: str
    correta: bool

# 🔹 Modelo de saída
class RespostaProvaOut(BaseModel):
    id: int
    prova_id: int
    pergunta_id: int
    resposta_aluno: str
    correta: bool

    class Config:
        from_attributes = True

# 🔸 Enviar respostas da prova
@router.post("/", response_model=RespostaProvaOut)
def responder_prova(resposta: RespostaProvaIn, db: Session = Depends(get_db)):
    prova = db.query(Prova).filter(Prova.id == resposta.prova_id).first()
    if not prova:
        raise HTTPException(status_code=404, detail="Prova não encontrada")

    nova = RespostaProva(
        prova_id=resposta.prova_id,
        pergunta_id=resposta.pergunta_id,
        resposta_dada=resposta.resposta_aluno,
        correta="sim" if resposta.correta else "não"
    )

    try:
        db.add(nova)
        db.commit()
        db.refresh(nova)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Erro ao salvar resposta: {str(e)}")

    return RespostaProvaOut(
        id=nova.id,
        prova_id=nova.prova_id,
        pergunta_id=nova.pergunta_id,
        resposta_aluno=nova.resposta_dada,
        correta=nova.correta.strip().lower() == "sim"
    )

# 🔸 Listar respostas de uma prova
@router.get("/{prova_id}", response_model=List[RespostaProvaOut])
def listar_respostas(prova_id: int, db: Session = Depends(get_db)):
    respostas = db.query(RespostaProva).filter(RespostaProva.prova_id == prova_id).all()
    return [
        RespostaProvaOut(
            id=r.id,
            prova_id=r.prova_id,
            pergunta_id=r.pergunta_id,
            resposta_aluno=r.resposta_dada,
            correta=r.correta.strip().lower() == "sim"
        )
        for r in respostas
    ]
