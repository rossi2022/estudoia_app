from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.db import get_db
from backend.database.models import Prova, AlertaProva
from datetime import datetime, timedelta

router = APIRouter(
    prefix="/agenda-provas",  # 🔁 atualizado de "/provas" para "/agenda-provas"
    tags=["Agenda de Provas"]
)

# 📌 Criar prova e agendar alertas
@router.post("/", status_code=201)
def criar_prova(dados: dict, db: Session = Depends(get_db)):
    aluno_id = dados.get("aluno_id")
    nome = dados.get("nome")
    data_prova_str = dados.get("data_prova")
    conteudo = dados.get("conteudo")

    if not all([aluno_id, nome, data_prova_str, conteudo]):
        raise HTTPException(status_code=400, detail="Dados incompletos para criação de prova.")

    try:
        data_prova = datetime.fromisoformat(data_prova_str)
    except ValueError:
        raise HTTPException(status_code=400, detail="Formato de data_prova inválido. Use ISO 8601.")

    nova_prova = Prova(
        aluno_id=aluno_id,
        nome=nome,
        data_prova=data_prova,
        conteudo=conteudo
    )
    db.add(nova_prova)
    db.commit()
    db.refresh(nova_prova)

    # ⏰ Agendar alertas: 7, 3 e 1 dias antes
    for dias in [7, 3, 1]:
        data_alerta = data_prova - timedelta(days=dias)
        if data_alerta > datetime.utcnow():
            alerta = AlertaProva(
                data_alerta=data_alerta,
                mensagem=f"Lembrete: Prova '{nome}' em {data_prova.strftime('%d/%m/%Y %H:%M')}",
                tipo_alerta=f"{dias}_dias_antes",
                prova_id=nova_prova.id
            )
            db.add(alerta)
    db.commit()

    return {
        "id": nova_prova.id,
        "nome": nova_prova.nome,
        "data_prova": nova_prova.data_prova,
        "conteudo": nova_prova.conteudo
    }

# 📚 Listar agenda de provas de um aluno
@router.get("/{aluno_id}")
def listar_agenda(aluno_id: int, db: Session = Depends(get_db)):  # 🔁 rota agora responde em /agenda-provas/{aluno_id}
    provas = db.query(Prova).filter(Prova.aluno_id == aluno_id).all()
    if not provas:
        raise HTTPException(status_code=404, detail="Nenhuma prova agendada para este aluno.")
    return {"agenda": [
        {"id": p.id, "nome": p.nome, "data_prova": p.data_prova, "conteudo": p.conteudo}
        for p in provas
    ]}

# 🔔 Listar alertas futuros para um aluno
@router.get("/alertas/{aluno_id}")
def listar_alertas(aluno_id: int, db: Session = Depends(get_db)):
    alertas = (
        db.query(AlertaProva)
          .join(Prova)
          .filter(Prova.aluno_id == aluno_id)
          .filter(AlertaProva.data_alerta >= datetime.utcnow())
          .all()
    )
    if not alertas:
        raise HTTPException(status_code=404, detail="Nenhum alerta futuro encontrado para este aluno.")
    return {"alertas": [
        {"id": a.id, "data_alerta": a.data_alerta, "mensagem": a.mensagem, "tipo": a.tipo_alerta, "prova_id": a.prova_id}
        for a in alertas
    ]}
