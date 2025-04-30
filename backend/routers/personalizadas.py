from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from backend.db import get_db
from backend.database.models import Aluno, HistoricoDesempenho
from backend.openai_api import gerar_perguntas_personalizadas

router = APIRouter()

@router.get("/{aluno_id}", response_model=List[str])
def perguntas_personalizadas(aluno_id: int, db: Session = Depends(get_db)):
    aluno = db.query(Aluno).filter(Aluno.id == aluno_id).first()
    if not aluno:
        raise HTTPException(status_code=404, detail="Aluno não encontrado")

    desempenho = (
        db.query(HistoricoDesempenho)
        .filter(HistoricoDesempenho.aluno_id == aluno_id)
        .all()
    )

    dados_desempenho = {
        d.materia: {
            "acertos": d.acertos,
            "erros": d.erros,
            "data": str(d.data)
        }
        for d in desempenho
    }

    perguntas = gerar_perguntas_personalizadas(dados_desempenho)
    return perguntas

