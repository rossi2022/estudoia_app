from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.db import get_db
from backend.database.models import Aluno, NotaMensal, Recompensa
from backend.schemas import RecompensaOut, RecompensaCreate

router = APIRouter(prefix="/recompensas", tags=["recompensas"])

# 🔹 ROTA GET já existente (mantida exatamente como estava)
@router.get("/{aluno_id}", response_model=RecompensaOut)
def gerar_recompensas(aluno_id: int, db: Session = Depends(get_db)):
    aluno = db.query(Aluno).filter(Aluno.id == aluno_id).first()

    if not aluno:
        raise HTTPException(status_code=404, detail="Aluno não encontrado")

    notas = db.query(NotaMensal).filter(NotaMensal.aluno_id == aluno_id).all()

    if notas is None or len(notas) == 0:
        return RecompensaOut(
            id=1,
            aluno_id=aluno.id,
            tipo="Inicial",
            descricao="🎓 Participação inicial",
            data="2025-04-01"
        )

    media_geral = sum(n.nota for n in notas) / len(notas)

    if media_geral >= 9.0:
        descricao = "🏆 Medalha de Excelência"
        tipo = "Excelência"
    elif media_geral >= 7.0:
        descricao = "🥇 Medalha de Ouro"
        tipo = "Ouro"
    elif media_geral >= 5.0:
        descricao = "🥈 Medalha de Prata"
        tipo = "Prata"
    else:
        descricao = "🥉 Medalha de Participação"
        tipo = "Participação"

    return RecompensaOut(
        id=1,
        aluno_id=aluno.id,
        tipo=tipo,
        descricao=descricao,
        data="2025-04-01"
    )

# ✅ NOVA ROTA POST para criar manualmente uma recompensa
@router.post("/criar", response_model=RecompensaOut)
def criar_recompensa(recompensa: RecompensaCreate, db: Session = Depends(get_db)):
    nova = Recompensa(**recompensa.dict())
    db.add(nova)
    db.commit()
    db.refresh(nova)
    return nova



