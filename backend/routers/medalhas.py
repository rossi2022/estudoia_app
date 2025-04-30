from fastapi import APIRouter, Depends, HTTPException 
from sqlalchemy.orm import Session
from backend.db import get_db  # ✅ corrigido
from backend.database.models import Aluno, Medalha  # ✅ corrigido
from backend.schemas import MedalhaOut, MedalhasDoAluno  # ✅ corrigido

router = APIRouter(prefix="/medalhas", tags=["Medalhas"])

@router.get("/medalhas/{aluno_id}", response_model=MedalhasDoAluno)
def get_medalhas_do_aluno(aluno_id: int, db: Session = Depends(get_db)):
    aluno = db.query(Aluno).filter(Aluno.id == aluno_id).first()
    if not aluno:
        raise HTTPException(status_code=404, detail="Aluno não encontrado")

    medalhas = db.query(Medalha).filter(Medalha.aluno_id == aluno_id).all()
    return {
        "aluno_id": aluno.id,
        "nome": aluno.nome,
        "medalhas": medalhas
    }





