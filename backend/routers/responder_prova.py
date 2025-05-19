# File: backend/routers/responder_prova.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from backend.db import get_db
from backend.database.models import Prova, RespostaProva, QuestaoProva
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

    class Config:
        from_attributes = True

# 🔹 Modelo de saída
class RespostaProvaOut(BaseModel):
    id: int
    prova_id: int
    pergunta_id: int
    resposta_aluno: str
    correta: bool

    class Config:
        from_attributes = True

# 🔸 Enviar resposta de uma questão da prova
@router.post("/", response_model=RespostaProvaOut, status_code=status.HTTP_200_OK)
def responder_prova(resposta: RespostaProvaIn, db: Session = Depends(get_db)):
    # Verifica existência da prova
    prova = db.query(Prova).filter(Prova.id == resposta.prova_id).first()
    if not prova:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Prova não encontrada")

    # Cria e salva a resposta
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
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Erro ao salvar resposta: {e}")

    # Conta quantas respostas já foram dadas nesta prova
    total_respondidas = db.query(RespostaProva).filter(RespostaProva.prova_id == resposta.prova_id).count()
    # Determina total de questões da prova
    total_questoes = db.query(QuestaoProva).filter(QuestaoProva.prova_id == resposta.prova_id).count()

    # Se todas as questões foram respondidas, calcula e atualiza a nota final
    if total_questoes > 0 and total_respondidas >= total_questoes:
        corretas = db.query(RespostaProva).filter(
            RespostaProva.prova_id == resposta.prova_id,
            RespostaProva.correta == "sim"
        ).count()
        # Escala de 0 a 10
        nota_final = (corretas / total_questoes) * 10
        prova.nota_final = nota_final
        db.commit()

    return RespostaProvaOut(
        id=nova.id,
        prova_id=nova.prova_id,
        pergunta_id=nova.pergunta_id,
        resposta_aluno=nova.resposta_dada,
        correta=nova.correta.strip().lower() == "sim"
    )

# 🔸 Listar respostas de uma prova
@router.get("/{prova_id}", response_model=List[RespostaProvaOut], status_code=status.HTTP_200_OK)
def listar_respostas(prova_id: int, db: Session = Depends(get_db)):
    respostas = db.query(RespostaProva).filter(RespostaProva.prova_id == prova_id).all()
    return [
        RespostaProvaOut(
            id=r.id,
            prova_id=r.prova_id,
            pergunta_id=r.pergunta_id,
            resposta_aluno=r.resposta_dada,
            correta=r.correta.strip().lower() == "sim"
        ) for r in respostas
    ]
