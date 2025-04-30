# backend/routers/historico_estudos.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.db import get_db
from backend.database.models import ProvaPersonalizada, Trabalho
from datetime import datetime

router = APIRouter(
    prefix="/historico",
    tags=["Histórico de Estudos"]
)

# 📚 Listar Provas Respondidas
@router.get("/provas/feitas")
def listar_provas_feitas(db: Session = Depends(get_db)):
    provas = db.query(ProvaPersonalizada).all()

    if not provas:
        raise HTTPException(status_code=404, detail="Nenhuma prova encontrada.")

    lista_provas = []
    for prova in provas:
        lista_provas.append({
            "id": prova.id,
            "titulo": prova.titulo,
            "descricao": prova.descricao,
            "data_entrega": prova.data_entrega
        })

    return {"provas_feitas": lista_provas}


# 📚 Listar Trabalhos Entregues
@router.get("/trabalhos/entregues")
def listar_trabalhos_entregues(db: Session = Depends(get_db)):
    trabalhos = db.query(Trabalho).all()

    if not trabalhos:
        raise HTTPException(status_code=404, detail="Nenhum trabalho encontrado.")

    lista_trabalhos = []
    for trabalho in trabalhos:
        lista_trabalhos.append({
            "id": trabalho.id,
            "titulo": trabalho.titulo,
            "tema": trabalho.tema,
            "prazo_entrega": trabalho.prazo_entrega
        })

    return {"trabalhos_entregues": lista_trabalhos}
