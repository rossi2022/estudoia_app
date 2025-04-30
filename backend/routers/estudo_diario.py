from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.db import get_db
from backend.database.models import EstudoDiario, Aluno
from pydantic import BaseModel, ConfigDict
from datetime import date, timedelta

# ▪️ Tira o prefix daqui
router = APIRouter(
    tags=["Modo Estudo Diário"]
)

class CheckinOut(BaseModel):
    aluno_id: int
    data: date
    model_config = ConfigDict(from_attributes=True)

# 🔹 POST /modo_estudo/{aluno_id}/checkin
@router.post("/{aluno_id}/checkin", response_model=CheckinOut, status_code=201)
def checkin_estudo(aluno_id: int, db: Session = Depends(get_db)):
    aluno = db.query(Aluno).filter(Aluno.id == aluno_id).first()
    if not aluno:
        raise HTTPException(status_code=404, detail="Aluno não encontrado")
    hoje = date.today()
    existente = (
        db.query(EstudoDiario)
          .filter(EstudoDiario.aluno_id == aluno_id, EstudoDiario.data == hoje)
          .first()
    )
    if existente:
        return existente
    novo = EstudoDiario(aluno_id=aluno_id, data=hoje)
    db.add(novo)
    db.commit()
    db.refresh(novo)
    return novo

# 🔹 GET /modo_estudo/{aluno_id}/streak
@router.get("/{aluno_id}/streak")
def get_streak(aluno_id: int, db: Session = Depends(get_db)):
    hoje = date.today()
    streak = 0
    dia = hoje
    while True:
        registro = (
            db.query(EstudoDiario)
              .filter(EstudoDiario.aluno_id == aluno_id, EstudoDiario.data == dia)
              .first()
        )
        if not registro:
            break
        streak += 1
        dia -= timedelta(days=1)
    return {"streak": streak}






