from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.db import get_db
from backend.database.models import HistoricoDesempenho, Aluno
from pydantic import BaseModel, ConfigDict
from typing import Dict
from datetime import date
from collections import defaultdict

router = APIRouter(
    prefix="/progresso",  # ✅ Adicionado prefixo para funcionar em /api/progresso
    tags=["progresso"]
)

# 🔹 Schema para criar progresso
class ProgressoCreate(BaseModel):
    aluno_id: int
    materia: str
    acertos: int
    erros: int

# 🔹 Schema para exibir progresso individual
class ProgressoOut(BaseModel):
    aluno_id: int
    materia: str
    acertos: int
    erros: int
    data: date

    model_config = ConfigDict(from_attributes=True)

# 🔹 Salvar progresso do aluno
@router.post("/salvar", response_model=ProgressoOut, status_code=201)
def salvar_progresso(dados: ProgressoCreate, db: Session = Depends(get_db)):
    aluno = db.query(Aluno).filter(Aluno.id == dados.aluno_id).first()
    if not aluno:
        raise HTTPException(status_code=404, detail="Aluno não encontrado")
    progresso = HistoricoDesempenho(**dados.dict())
    db.add(progresso)
    db.commit()
    db.refresh(progresso)
    return progresso

# 🔹 Listar média de acertos por matéria (0–10)
@router.get("/{aluno_id}", response_model=Dict[str, float])
def listar_progresso(aluno_id: int, db: Session = Depends(get_db)) -> Dict[str, float]:
    historico = (
        db.query(HistoricoDesempenho)
          .filter(HistoricoDesempenho.aluno_id == aluno_id)
          .all()
    )

    if not historico:
        return {}

    notas_por_mat: Dict[str, list[float]] = defaultdict(list)
    for h in historico:
        total = h.acertos + h.erros
        if total > 0:
            nota = (h.acertos / total) * 10
            notas_por_mat[h.materia].append(nota)

    medias = {
        materia: round(sum(vals) / len(vals), 2)
        for materia, vals in notas_por_mat.items()
    }
    return medias

# 🔹 Listar progresso geral (nota média total)
@router.get("/geral/{aluno_id}")
def progresso_geral(aluno_id: int, db: Session = Depends(get_db)):
    historico = (
        db.query(HistoricoDesempenho)
          .filter(HistoricoDesempenho.aluno_id == aluno_id)
          .all()
    )

    total_acertos = sum(h.acertos for h in historico)
    total_erros = sum(h.erros for h in historico)
    total = total_acertos + total_erros

    if total == 0:
        return {"media_geral": 0.0}

    media = round((total_acertos / total) * 10, 2)
    return {"media_geral": media}



















