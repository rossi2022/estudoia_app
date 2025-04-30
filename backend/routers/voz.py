from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse

router = APIRouter()

@router.post("/avaliar")
async def avaliar_leitura(arquivo_audio: UploadFile = File(...)):
    # 🔸 Verifica se o arquivo é válido e tem conteúdo
    if not arquivo_audio or not arquivo_audio.filename.endswith(".wav"):
        raise HTTPException(status_code=400, detail="Arquivo inválido. Envie um arquivo .wav")

    conteudo = await arquivo_audio.read()
    if not conteudo:
        raise HTTPException(status_code=400, detail="Arquivo está vazio")

    # Simulação de retorno da IA
    resposta_ia = {
        "fluencia": "Boa",
        "entonacao": "Clara",
        "comentario": "Continue praticando para melhorar ainda mais!"
    }

    return JSONResponse(content=resposta_ia)



