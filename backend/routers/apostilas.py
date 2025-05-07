# backend/routers/apostilas.py

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from backend.db import get_db
from backend.database.models import Apostila

router = APIRouter(
    prefix="/apostilas",  # ✅ Prefixo adicionado para evitar conflito com rotas dinâmicas
    tags=["Apostilas"]
)

@router.get("/", summary="Listar todas as apostilas")
def listar_apostilas(db: Session = Depends(get_db)):
    """
    Retorna a lista de todas as apostilas disponíveis no banco de dados.
    """
    return db.query(Apostila).all()
