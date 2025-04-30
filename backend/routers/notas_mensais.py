from fastapi import APIRouter, Depends, HTTPException 
from sqlalchemy.orm import Session
from typing import List
from backend.db import SessionLocal  # ✅ Conexão com banco
from backend.database.models import NotaMensal  # ✅ Modelo correto
from backend.schemas import NotaMensalCreate, NotaMensalOut  # ✅ Schemas corretos

router = APIRouter(
    prefix="/notas_mensais",
    tags=["Notas Mensais"]
)

# 🔹 Dependência de banco de dados
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 🔹 Rota POST para registrar nova nota mensal
@router.post("/", response_model=NotaMensalOut, status_code=201)
def registrar_nota_mensal(nota: NotaMensalCreate, db: Session = Depends(get_db)):
    try:
        nova_nota = NotaMensal(**nota.dict())
        db.add(nova_nota)
        db.commit()
        db.refresh(nova_nota)
        return nova_nota
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Erro ao registrar nota: {str(e)}")

# 🔹 Rota GET para listar todas as notas mensais de um aluno
@router.get("/{aluno_id}", response_model=List[NotaMensalOut])
def listar_notas_mensais(aluno_id: int, db: Session = Depends(get_db)):
    try:
        notas = db.query(NotaMensal).filter(NotaMensal.aluno_id == aluno_id).all()
        return notas
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao buscar notas: {str(e)}")


       
