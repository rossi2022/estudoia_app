# backend/routers/notas_gerais.py

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from backend.db import SessionLocal
from backend.database.models import NotaMensal
from backend.schemas import NotaMensalCreate, NotaMensalOut

router = APIRouter(
    prefix="/notas",
    tags=["Notas"]
)

# Dependência de banco de dados
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Rota compatível com POST /notas
@router.post("/", response_model=NotaMensalOut)
def registrar_nota(nota: NotaMensalCreate, db: Session = Depends(get_db)):
    nova_nota = NotaMensal(**nota.dict())
    db.add(nova_nota)
    db.commit()
    db.refresh(nova_nota)
    return nova_nota





