# File: backend/routers/materias.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List, Optional

from backend.db import get_db
from backend.database.models import Materia

router = APIRouter(
    prefix="/materias",
    tags=["Materias"]
)

# 🔸 Schema de saída
class MateriaOut(BaseModel):
    nome: str
    apostila_url: Optional[str] = None

    class Config:
        from_attributes = True

# 🔸 Schema de entrada
class AtualizarApostila(BaseModel):
    nome: str
    apostila_url: str

# ✅ Listar todas as matérias do banco
@router.get("/", response_model=List[MateriaOut])
def listar_materias(db: Session = Depends(get_db)):
    return db.query(Materia).all()

# ✅ Atualizar ou criar apostila para uma matéria
@router.post("/apostila")
def atualizar_apostila(dados: AtualizarApostila, db: Session = Depends(get_db)):
    materia = db.query(Materia).filter_by(nome=dados.nome).first()
    if materia:
        materia.apostila_url = dados.apostila_url
        msg = "Apostila atualizada com sucesso."
    else:
        materia = Materia(nome=dados.nome, apostila_url=dados.apostila_url)
        db.add(materia)
        msg = "Matéria criada com apostila."

    db.commit()
    return {
        "message": msg,
        "materia": {
            "nome": materia.nome,
            "apostila_url": materia.apostila_url
        }
    }
