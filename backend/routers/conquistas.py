# File: backend/routers/conquistas.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from backend.db import get_db
from backend.database.models import Conquista, Aluno
from backend.schemas import ConquistaOut, ConquistaCreate

router = APIRouter(
    prefix="/conquistas",
    tags=["Conquistas"]
)

@router.post("/", response_model=ConquistaOut, status_code=status.HTTP_201_CREATED)
def criar_conquista(conquista: ConquistaCreate, db: Session = Depends(get_db)):
    aluno = db.query(Aluno).filter(Aluno.id == conquista.aluno_id).first()
    if not aluno:
        raise HTTPException(status_code=404, detail="Aluno não encontrado")
    db_conquista = Conquista(**conquista.dict())
    db.add(db_conquista)
    db.commit()
    db.refresh(db_conquista)
    return db_conquista

@router.get("/listar/{aluno_id}", response_model=list[ConquistaOut])
def listar_conquistas(aluno_id: int, db: Session = Depends(get_db)):
    aluno = db.query(Aluno).filter(Aluno.id == aluno_id).first()
    if not aluno:
        raise HTTPException(status_code=404, detail="Aluno não encontrado")
    return db.query(Conquista).filter(Conquista.aluno_id == aluno_id).all()

@router.get("/mural/{aluno_id}", response_model=list[ConquistaOut])
def listar_mural(aluno_id: int, db: Session = Depends(get_db)):
    aluno = db.query(Aluno).filter(Aluno.id == aluno_id).first()
    if not aluno:
        raise HTTPException(status_code=404, detail="Aluno não encontrado")
    return db.query(Conquista).filter(Conquista.aluno_id == aluno_id).all()

# ✅ Rota adicional necessária para o frontend
@router.get("/{aluno_id}", response_model=list[ConquistaOut])
def conquistas_frontend(aluno_id: int, db: Session = Depends(get_db)):
    aluno = db.query(Aluno).filter(Aluno.id == aluno_id).first()
    if not aluno:
        raise HTTPException(status_code=404, detail="Aluno não encontrado")
    return db.query(Conquista).filter(Conquista.aluno_id == aluno_id).all()




