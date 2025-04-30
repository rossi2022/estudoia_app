# backend/routers/provas_trabalhos.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.db import get_db
from backend.database.models import ProvaPersonalizada, Trabalho
from datetime import datetime  # 🔹 Importante para conversão de datas

router = APIRouter(
    prefix="/professor",
    tags=["Provas e Trabalhos"]
)

# 📚 Criar Prova Personalizada
@router.post("/provas/criar")
def criar_prova(titulo: str, descricao: str = None, data_entrega: str = None, professor_id: int = 1, db: Session = Depends(get_db)):
    data_entrega_date = None
    if data_entrega:
        try:
            data_entrega_date = datetime.strptime(data_entrega, "%Y-%m-%d").date()
        except ValueError:
            raise HTTPException(status_code=400, detail="Data de entrega inválida. Use o formato YYYY-MM-DD.")

    nova_prova = ProvaPersonalizada(
        professor_id=professor_id,
        titulo=titulo,
        descricao=descricao,
        data_entrega=data_entrega_date
    )
    db.add(nova_prova)
    db.commit()
    db.refresh(nova_prova)

    return {"mensagem": "Prova personalizada criada com sucesso!", "prova_id": nova_prova.id}


# 📚 Criar Trabalho Acadêmico
@router.post("/trabalhos/criar")
def criar_trabalho(titulo: str, tema: str = None, prazo_entrega: str = None, professor_id: int = 1, db: Session = Depends(get_db)):
    prazo_entrega_date = None
    if prazo_entrega:
        try:
            prazo_entrega_date = datetime.strptime(prazo_entrega, "%Y-%m-%d").date()
        except ValueError:
            raise HTTPException(status_code=400, detail="Prazo de entrega inválido. Use o formato YYYY-MM-DD.")

    novo_trabalho = Trabalho(
        professor_id=professor_id,
        titulo=titulo,
        tema=tema,
        prazo_entrega=prazo_entrega_date
    )
    db.add(novo_trabalho)
    db.commit()
    db.refresh(novo_trabalho)

    return {"mensagem": "Trabalho criado com sucesso!", "trabalho_id": novo_trabalho.id}
