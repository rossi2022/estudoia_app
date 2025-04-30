from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.db import get_db
from backend.database.models import Aluno
from backend.schemas import MotivacaoOut  # Esquema da resposta motivacional

router = APIRouter(
    prefix="/motivacao",  # Prefixo da rota
    tags=["Motivação"]
)

# 🔹 Endpoint GET para gerar motivação com aluno_id como parâmetro de URL
@router.get("/{aluno_id}", response_model=MotivacaoOut)
def gerar_motivacao(aluno_id: int, db: Session = Depends(get_db)):
    aluno = db.query(Aluno).filter(Aluno.id == aluno_id).first()

    if not aluno:
        raise HTTPException(status_code=404, detail="Aluno não encontrado")

    # Lógica para gerar a mensagem motivacional
    mensagem = f"Parabéns, {aluno.nome}! Você está indo muito bem! Continue assim!"
    
    return MotivacaoOut(
        aluno_id=aluno.id,
        mensagem=mensagem
    )





