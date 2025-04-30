# backend/routers/tarefas_estudo.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.db import get_db
from backend.database.models import TarefaEstudo
from pydantic import BaseModel
from typing import List
from datetime import date

router = APIRouter(
    prefix="/tarefas_estudo",
    tags=["Tarefas de Estudo"]
)

# 📌 Modelo para criar tarefa
class TarefaCreate(BaseModel):
    aluno_id: int
    data: date
    topicos: str

# 📌 Modelo para resposta de tarefa
class TarefaOut(BaseModel):
    id: int
    aluno_id: int
    data: date
    topicos: str
    status: str

    class Config:
        from_attributes = True

# 📌 Modelo para atualizar status
class TarefaStatusUpdate(BaseModel):
    status: str

# 📌 POST: Criar nova tarefa
@router.post("/", response_model=TarefaOut)
def criar_tarefa(tarefa: TarefaCreate, db: Session = Depends(get_db)):
    nova_tarefa = TarefaEstudo(
        aluno_id=tarefa.aluno_id,
        data=tarefa.data,
        topicos=tarefa.topicos,
        status="pendente"
    )
    db.add(nova_tarefa)
    db.commit()
    db.refresh(nova_tarefa)
    return nova_tarefa

# 📌 GET: Listar tarefas de um aluno
@router.get("/{aluno_id}", response_model=List[TarefaOut])
def listar_tarefas(aluno_id: int, db: Session = Depends(get_db)):
    tarefas = db.query(TarefaEstudo).filter_by(aluno_id=aluno_id).all()
    return tarefas

# 📌 PUT: Atualizar uma tarefa existente
@router.put("/{tarefa_id}", response_model=TarefaOut)
def atualizar_tarefa(tarefa_id: int, tarefa: TarefaCreate, db: Session = Depends(get_db)):
    tarefa_existente = db.query(TarefaEstudo).filter_by(id=tarefa_id).first()
    if not tarefa_existente:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada")

    tarefa_existente.aluno_id = tarefa.aluno_id
    tarefa_existente.data = tarefa.data
    tarefa_existente.topicos = tarefa.topicos
    db.commit()
    db.refresh(tarefa_existente)
    return tarefa_existente

# 📌 PATCH: Atualizar apenas o status da tarefa
@router.patch("/{tarefa_id}/status", response_model=TarefaOut)
def atualizar_status_tarefa(tarefa_id: int, status_update: TarefaStatusUpdate, db: Session = Depends(get_db)):
    tarefa = db.query(TarefaEstudo).filter_by(id=tarefa_id).first()
    if not tarefa:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada")
    tarefa.status = status_update.status
    db.commit()
    db.refresh(tarefa)
    return tarefa

# 📌 DELETE: Deletar tarefa
@router.delete("/{tarefa_id}")
def deletar_tarefa(tarefa_id: int, db: Session = Depends(get_db)):
    tarefa = db.query(TarefaEstudo).filter_by(id=tarefa_id).first()
    if not tarefa:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada")
    db.delete(tarefa)
    db.commit()
    return {"mensagem": "Tarefa deletada com sucesso!"}







