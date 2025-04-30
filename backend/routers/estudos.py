# backend/routers/estudos.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.db import get_db
from backend.database.models import ProvaPersonalizada, Trabalho, EntregaTrabalho  # ✅ Adicionado
from datetime import datetime  # ✅ Já estava

router = APIRouter(
    prefix="/estudos",
    tags=["Área de Estudos"]
)

# 📚 Listar todas as provas disponíveis
@router.get("/provas")
def listar_provas(db: Session = Depends(get_db)):
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

    return {"provas": lista_provas}

# 📚 Listar todos os trabalhos disponíveis
@router.get("/trabalhos")
def listar_trabalhos(db: Session = Depends(get_db)):
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

    return {"trabalhos": lista_trabalhos}

# 📚 Entregar Trabalho Acadêmico (agora salvando no banco)
@router.post("/trabalhos/{trabalho_id}/entregar")
def entregar_trabalho(trabalho_id: int, resposta: dict, db: Session = Depends(get_db)):
    trabalho = db.query(Trabalho).filter(Trabalho.id == trabalho_id).first()

    if not trabalho:
        raise HTTPException(status_code=404, detail="Trabalho não encontrado.")

    texto_resposta = resposta.get("resposta")
    aluno_id = resposta.get("aluno_id")

    if not texto_resposta or not aluno_id:
        raise HTTPException(status_code=400, detail="Resposta ou aluno_id não enviados.")

    # 📌 Agora realmente salvando a entrega
    nova_entrega = EntregaTrabalho(
        trabalho_id=trabalho_id,
        aluno_id=aluno_id,
        resposta=texto_resposta,
        data_entrega=datetime.utcnow()
    )
    db.add(nova_entrega)
    db.commit()
    db.refresh(nova_entrega)

    return {
        "mensagem": "Trabalho entregue e registrado com sucesso!",
        "entrega_id": nova_entrega.id,
        "data_entrega": nova_entrega.data_entrega
    }


