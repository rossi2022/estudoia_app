# File: backend/routers/relatorio.py 

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.db import get_db  # ✅ corrigido
from backend.database.models import Aluno, NotaMensal  # ✅ corrigido
from backend.schemas import RelatorioMensalOut  # ✅ corrigido
from pydantic import BaseModel
from datetime import datetime

router = APIRouter(
    prefix="/relatorio",
    tags=["relatorio"]
)

@router.get("/{aluno_id}", response_model=RelatorioMensalOut)
def gerar_relatorio(aluno_id: int, db: Session = Depends(get_db)):
    aluno = db.query(Aluno).filter(Aluno.id == aluno_id).first()
    if not aluno:
        raise HTTPException(status_code=404, detail="Aluno não encontrado")

    notas = db.query(NotaMensal).filter(NotaMensal.aluno_id == aluno_id).all()
    media_geral = sum(n.nota for n in notas) / len(notas) if notas else 0.0

    if media_geral >= 9.0:
        mensagem = "Excelente trabalho! Continue assim! 🏆"
    elif media_geral >= 7.0:
        mensagem = "Muito bem! Você está indo no caminho certo! 👏"
    elif media_geral >= 5.0:
        mensagem = "Você consegue melhorar, mantenha o foco! 💪"
    else:
        mensagem = "Vamos juntos reforçar seu aprendizado! Não desista! 🚀"

    return RelatorioMensalOut(
        aluno_id=aluno.id,
        nome=aluno.nome,
        email=aluno.email,
        foto_url=aluno.foto_url,
        media_geral=media_geral,
        mensagem_motivacional=mensagem
    )

# ✅ Novo resumo diário
class ResumoDiarioOut(BaseModel):
    data: str
    mensagem: str

@router.get("/resumo/{aluno_id}", response_model=ResumoDiarioOut)
def resumo_diario(aluno_id: int):
    # Simulação de mensagem motivacional para o dia
    return {
        "data": datetime.today().strftime("%Y-%m-%d"),
        "mensagem": f"Resumo do dia para o aluno {aluno_id}: Estudo realizado com sucesso e foco mantido! 📚"
    }







