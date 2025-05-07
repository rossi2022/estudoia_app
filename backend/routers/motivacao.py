# File: backend/routers/motivacao.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.db import get_db
from backend.database.models import Aluno
from pydantic import BaseModel
from typing import List

router = APIRouter(
    prefix="/motivacao",
    tags=["Motivacao"]
)

# 🔹 Modelo de resposta
class SugestoesOut(BaseModel):
    mensagens: List[str]

# 🔹 GET /motivacao/sugestoes/{aluno_id}
@router.get("/sugestoes/{aluno_id}", response_model=SugestoesOut)
def sugestoes_ia(aluno_id: int, db: Session = Depends(get_db)):
    aluno = db.query(Aluno).filter(Aluno.id == aluno_id).first()
    if not aluno:
        raise HTTPException(status_code=404, detail="Aluno não encontrado")

    sugestoes = [
        f"Parabéns pelo seu esforço, {aluno.nome}! Continue assim!",
        "Lembre-se: o conhecimento é uma construção diária.",
        "Estude um pouco a cada dia e você irá longe.",
        "Acredite no seu potencial. Você é capaz!",
        "Seus resultados refletem sua dedicação. Continue evoluindo!"
    ]

    return {"mensagens": sugestoes}



