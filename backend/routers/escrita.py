# backend/routers/escrita.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.db import get_db
from backend.database.models import EscritaCriativa, Aluno
from backend.schemas import EscritaCriativaCreate, EscritaCriativaOut
from datetime import date

router = APIRouter()

@router.post("/", response_model=EscritaCriativaOut)
def criar_escrita(escrita: EscritaCriativaCreate, db: Session = Depends(get_db)):
    aluno = db.query(Aluno).filter(Aluno.id == escrita.aluno_id).first()
    if not aluno:
        raise HTTPException(status_code=404, detail="Aluno não encontrado")

    nova_escrita = EscritaCriativa(
        aluno_id=escrita.aluno_id,
        tema=escrita.tema,
        texto=escrita.texto,
        feedback="Obrigado por enviar seu texto! Em breve você receberá uma avaliação da IA.",
        data_envio=date.today()
    )

    db.add(nova_escrita)
    db.commit()
    db.refresh(nova_escrita)
    return nova_escrita

@router.get("/{aluno_id}", response_model=list[EscritaCriativaOut])
def listar_escritas(aluno_id: int, db: Session = Depends(get_db)):
    escritas = db.query(EscritaCriativa).filter(EscritaCriativa.aluno_id == aluno_id).all()
    return escritas



