from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.db import get_db
from backend.database.models import Aluno, NotaMensal

router = APIRouter(
    prefix="/relatorio",
    tags=["Relatório"],
    responses={404: {"description": "Não encontrado"}},
)

# 🔹 Gerar relatório simples de notas do aluno
@router.get("/notas/{aluno_id}")
def gerar_relatorio_notas(aluno_id: int, db: Session = Depends(get_db)):
    aluno = db.query(Aluno).filter(Aluno.id == aluno_id).first()
    if not aluno:
        raise HTTPException(status_code=404, detail="Aluno não encontrado.")
    
    notas = db.query(NotaMensal).filter(NotaMensal.aluno_id == aluno_id).all()
    if not notas:
        raise HTTPException(status_code=404, detail="Nenhuma nota encontrada para o aluno.")

    relatorio = {
        "aluno": aluno.nome,
        "notas": [
            {
                "materia": nota.materia,
                "nota": nota.nota,
                "mes": nota.mes
            }
            for nota in notas
        ]
    }

    return relatorio




