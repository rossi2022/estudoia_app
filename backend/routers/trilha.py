from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from backend.db import get_db
from backend.database.models import TrilhaAprendizado
from pydantic import BaseModel
from pydantic.config import ConfigDict

router = APIRouter()

# 🔹 Esquema de entrada
class TrilhaIn(BaseModel):
    aluno_id: int
    titulo: str
    descricao: str
    habilidade: str

# 🔹 Esquema de saída
class TrilhaOut(BaseModel):
    id: int
    aluno_id: int
    titulo: str
    descricao: str
    habilidade: str
    status: str

    model_config = ConfigDict(from_attributes=True)

# 🔸 Criar trilha
@router.post("/trilha/", response_model=TrilhaOut)
def criar_trilha(trilha: TrilhaIn, db: Session = Depends(get_db)):
    nova = TrilhaAprendizado(**trilha.model_dump(), status="pendente")
    db.add(nova)
    db.commit()
    db.refresh(nova)
    return nova

# 🔸 Listar trilhas de um aluno
@router.get("/trilha/{aluno_id}", response_model=list[TrilhaOut])
def listar_trilhas(aluno_id: int, db: Session = Depends(get_db)):
    return db.query(TrilhaAprendizado).filter(TrilhaAprendizado.aluno_id == aluno_id).all()

# 🔸 Concluir trilha
@router.put("/trilha/{trilha_id}/concluir", response_model=TrilhaOut)
def concluir_trilha(trilha_id: int, db: Session = Depends(get_db)):
    trilha = db.query(TrilhaAprendizado).filter(TrilhaAprendizado.id == trilha_id).first()
    if not trilha:
        raise HTTPException(status_code=404, detail="Trilha não encontrada")
    trilha.status = "concluída"
    db.commit()
    db.refresh(trilha)
    return trilha


