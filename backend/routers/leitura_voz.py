# backend/routers/leitura_voz.py
from fastapi import APIRouter, UploadFile, File, HTTPException
from backend.utils.avaliador_audio import avaliar_leitura_voz  # novo utilitário de IA

router = APIRouter(prefix="/leitura-voz", tags=["Leitura em Voz Alta"])

@router.post("/avaliar/{aluno_id}")
async def avaliar_audio_leitura(aluno_id: int, arquivo: UploadFile = File(...)):
    if not arquivo.filename.endswith(".wav"):
        raise HTTPException(status_code=400, detail="Envie um arquivo .wav válido")

    conteudo = await arquivo.read()
    resultado = avaliar_leitura_voz(aluno_id, conteudo)
    return {"feedback": resultado}
