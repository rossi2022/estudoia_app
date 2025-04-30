# File: backend/routers/prova.py

from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.db import get_db
from backend.database.models import Prova, QuestaoProva, RespostaProva, Pergunta
from backend import schemas

# ▪️ Tira o prefix daqui, deixando só as tags
router = APIRouter(
    tags=["Provas"]
)

# 🔹 Listar todas as provas de um aluno
@router.get("/{aluno_id}", response_model=List[schemas.ProvaOut])
def listar_provas(aluno_id: int, db: Session = Depends(get_db)):
    provas = db.query(Prova).filter(Prova.aluno_id == aluno_id).all()
    return provas

@router.post("/gerar", response_model=schemas.ProvaOut)
def gerar_prova(data: schemas.GerarProvaRequest, db: Session = Depends(get_db)):
    perguntas_disponiveis = db.query(Pergunta).filter(Pergunta.materia == data.materia).all()
    if not perguntas_disponiveis:
        raise HTTPException(status_code=404, detail="Nenhuma pergunta disponível para esta matéria.")
    questoes = [QuestaoProva(pergunta_id=p.id) for p in perguntas_disponiveis[:5]]
    prova = Prova(aluno_id=data.aluno_id, questoes=questoes)
    db.add(prova)
    db.commit()
    db.refresh(prova)
    return prova

@router.post("/responder", response_model=schemas.ResultadoProvaOut)
def responder_prova(respostas: List[schemas.RespostaProvaCreate], db: Session = Depends(get_db)):
    nota = 0
    for resposta in respostas:
        pergunta = db.query(Pergunta).get(resposta.pergunta_id)
        if not pergunta:
            raise HTTPException(status_code=404, detail=f"Pergunta ID {resposta.pergunta_id} não encontrada.")
        if pergunta.resposta_correta.strip().lower() == resposta.resposta.strip().lower():
            nota += 1
        db.add(RespostaProva(
            prova_id=resposta.prova_id,
            pergunta_id=resposta.pergunta_id,
            resposta=resposta.resposta
        ))
    db.commit()
    return schemas.ResultadoProvaOut(
        prova_id=respostas[0].prova_id if respostas else 0,
        nota=nota
    )

@router.get("/gerar/{aluno_id}", response_model=schemas.ProvaOut)
def gerar_prova_get(aluno_id: int, db: Session = Depends(get_db)):
    materia_padrao = "História"
    perguntas = db.query(Pergunta).filter(Pergunta.materia == materia_padrao).all()
    if not perguntas:
        raise HTTPException(status_code=404, detail="Nenhuma pergunta disponível para esta matéria.")
    questoes = [QuestaoProva(pergunta_id=p.id) for p in perguntas[:5]]
    prova = Prova(aluno_id=aluno_id, questoes=questoes)
    db.add(prova)
    db.commit()
    db.refresh(prova)
    return prova

















