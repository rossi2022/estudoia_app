# File: backend/routers/perguntas.py

from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import Optional, List

from backend.db import get_db
from backend.database.models import Pergunta
from backend.schemas import PerguntaCreate, PerguntaOut

router = APIRouter(
    prefix="/perguntas",
    tags=["perguntas"]
)

# ✅ Criar nova pergunta
@router.post(
    "/criar",
    response_model=PerguntaOut,
    status_code=status.HTTP_201_CREATED
)
def criar_pergunta(pergunta: PerguntaCreate, db: Session = Depends(get_db)):
    nova = Pergunta(
        materia=pergunta.materia,
        enunciado=pergunta.enunciado,
        resposta_correta=pergunta.resposta_correta,
        dificuldade=pergunta.dificuldade or "media"
    )
    db.add(nova)
    db.commit()
    db.refresh(nova)
    return nova

# ✅ Listar perguntas (filtros opcionais)
@router.get(
    "/",
    response_model=List[PerguntaOut],
    status_code=status.HTTP_200_OK
)
def listar_perguntas(
    materia: Optional[str] = None,
    dificuldade: Optional[str] = None,
    db: Session = Depends(get_db)
):
    query = db.query(Pergunta)
    if materia:
        query = query.filter(Pergunta.materia == materia)
    if dificuldade:
        query = query.filter(Pergunta.dificuldade == dificuldade)
    return query.all()

# ✅ Obter uma pergunta aleatória
@router.get(
    "/aleatoria",
    response_model=PerguntaOut,
    status_code=status.HTTP_200_OK
)
def obter_pergunta_aleatoria(db: Session = Depends(get_db)):
    pergunta = db.query(Pergunta).order_by(func.random()).first()
    if not pergunta:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Nenhuma pergunta encontrada")
    return pergunta
































