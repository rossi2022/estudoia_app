# backend/routers/agenda.py
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
from backend.ai_module import gerar_agenda_estudos

router = APIRouter(prefix="/agenda", tags=["Agenda de Estudos"])

class DesempenhoAluno(BaseModel):
    resumo: str
    aluno_id: Optional[int] = None

@router.post("/gerar")
def gerar_agenda(dados: DesempenhoAluno):
    if not dados.resumo:
        raise HTTPException(status_code=400, detail="Resumo de desempenho é obrigatório")

    resultado = gerar_agenda_estudos(dados.resumo)
    return {"agenda": resultado}
