# backend/routers/mensagens.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.db import get_db
from backend.database.models import Aluno, HistoricoDesempenho
from backend.openai_api import gerar_mensagem_motivacional

router = APIRouter(prefix="/mensagens", tags=["Mensagens de Incentivo"])

@router.get("/{aluno_id}")
def mensagem_automatica(aluno_id: int, db: Session = Depends(get_db)):
    aluno = db.query(Aluno).filter(Aluno.id == aluno_id).first()
    if not aluno:
        raise HTTPException(status_code=404, detail="Aluno não encontrado")

    historico = db.query(HistoricoDesempenho).filter(HistoricoDesempenho.aluno_id == aluno_id).all()

    desempenho = {
        "nome": aluno.nome,
        "notas": {},
        "maiores_erros": {}
    }

    for h in historico:
        desempenho["notas"].setdefault(h.materia, {"acertos": 0, "erros": 0})
        desempenho["notas"][h.materia]["acertos"] += h.acertos
        desempenho["notas"][h.materia]["erros"] += h.erros

    mensagem = gerar_mensagem_motivacional(desempenho)
    return {"mensagem": mensagem}
