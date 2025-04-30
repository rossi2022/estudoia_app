from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from backend.openai_api import gerar_explicacao

router = APIRouter()

class ExplicacaoRequest(BaseModel):
    pergunta: str

@router.post("/", tags=["Explicação"])
def obter_explicacao(payload: ExplicacaoRequest):
    try:
        resposta = gerar_explicacao(payload.pergunta)
        return {"explicacao": resposta}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))




