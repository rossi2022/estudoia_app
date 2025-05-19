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

@router.post(
    "/criar",
    response_model=PerguntaOut,
    status_code=status.HTTP_201_CREATED
)
@router.post(
    "/",
    response_model=PerguntaOut,
    status_code=status.HTTP_201_CREATED
)
def criar_pergunta(pergunta: PerguntaCreate, db: Session = Depends(get_db)):
    """
    Cria uma nova pergunta.
    Endpoints disponíveis:
      - POST /api/perguntas/criar
      - POST /api/perguntas/
    """
    nova = Pergunta(
        materia=pergunta.materia,
        enunciado=pergunta.pergunta if hasattr(pergunta, 'pergunta') else pergunta.enunciado,
        resposta_correta=pergunta.resposta_correta,
        dificuldade=pergunta.dificuldade or "media"
    )
    db.add(nova)
    db.commit()
    db.refresh(nova)
    return PerguntaOut(
        id=nova.id,
        materia=nova.materia,
        enunciado=nova.enunciado,
        resposta_correta=nova.resposta_correta,
        dificuldade=nova.dificuldade
    )

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
    """
    Lista todas as perguntas, com filtros opcionais:
      GET /api/perguntas/?materia=...&dificuldade=...
    """
    query = db.query(Pergunta)
    if materia:
        query = query.filter(Pergunta.materia == materia)
    if dificuldade:
        query = query.filter(Pergunta.dificuldade == dificuldade)
    return query.all()

@router.get(
    "/aleatoria",
    response_model=PerguntaOut,
    status_code=status.HTTP_200_OK
)
def obter_pergunta_aleatoria(db: Session = Depends(get_db)):
    """
    Retorna uma pergunta aleatória.
      GET /api/perguntas/aleatoria
    """
    pergunta = db.query(Pergunta).order_by(func.random()).first()
    if not pergunta:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Nenhuma pergunta encontrada")
    return pergunta




























