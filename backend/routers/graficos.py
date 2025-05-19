# File: backend/routers/graficos.py

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func, case
from typing import Dict, Any, List

from backend.db import get_db
from backend.database.models import Prova, RespostaProva, Pergunta

router = APIRouter(
    prefix="/graficos",
    tags=["Graficos"]
)

@router.get("/desempenho/{aluno_id}", response_model=Dict[str, Any])
def desempenho(aluno_id: int, db: Session = Depends(get_db)):
    # Histórico de provas feitas (nota_final não nulo)
    provas = (
        db.query(Prova)
        .filter(Prova.aluno_id == aluno_id, Prova.nota_final != None)
        .order_by(Prova.data_prova)
        .all()
    )
    historico_estudos: List[Dict[str, Any]] = [
        {"data": p.data_prova.strftime("%Y-%m-%d"), "nota": p.nota_final}
        for p in provas
    ]

    # Cálculo da média por matéria: proporção de respostas corretas * 10
    q = (
        db.query(
            Pergunta.materia,
            func.avg(
                case((RespostaProva.correta == "sim", 1), else_=0)
            ) * 10
        )
        .join(RespostaProva, Pergunta.id == RespostaProva.pergunta_id)
        .join(Prova, RespostaProva.prova_id == Prova.id)
        .filter(Prova.aluno_id == aluno_id)
        .group_by(Pergunta.materia)
        .all()
    )
    media_por_materia: Dict[str, float] = {
        materia: round(avg or 0, 2) for materia, avg in q
    }

    return {
        "desempenho": {
            "media_por_materia": media_por_materia,
            "historico_estudos": historico_estudos
        }
    }


