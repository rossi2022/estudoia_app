# File: backend/routers/graficos.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from collections import defaultdict

from backend.db import get_db
from backend.database.models import HistoricoDesempenho

router = APIRouter(
    prefix="/graficos",
    tags=["Gráficos"]
)

@router.get("/desempenho/{aluno_id}")
def desempenho(aluno_id: int, db: Session = Depends(get_db)):
    """
    Retorna o histórico de acertos por matéria para o aluno.
    Se não houver dados, retorna um objeto vazio para permitir plotagem sem erros.
    """
    try:
        registros = db.query(HistoricoDesempenho).filter_by(aluno_id=aluno_id).all()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao acessar dados: {str(e)}")

    # Construir dicionário de desempenho agrupado por matéria
    desempenho_dict = defaultdict(list)
    for reg in registros:
        desempenho_dict[reg.materia].append({
            "data": reg.data.isoformat(),
            "acertos": reg.acertos,
            "erros": reg.erros
        })

    # Retornar o dicionário (converte defaultdict para dict)
    return {"desempenho": dict(desempenho_dict)}




