from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from backend.db import get_db
from backend.database.models import NotaMensal
from sqlalchemy import func

router = APIRouter()

# 🔹 Rota para pegar gráfico de desempenho (média de notas por matéria)
@router.get("/grafico/desempenho")
def grafico_desempenho(db: Session = Depends(get_db)):
    # Obter a média de notas por matéria
    resultado = db.query(
        NotaMensal.materia,
        func.avg(NotaMensal.nota).label("media_nota")
    ).group_by(NotaMensal.materia).all()

    # Retornando a média de notas por matéria
    return [{"materia": materia, "media_nota": media_nota} for materia, media_nota in resultado]






