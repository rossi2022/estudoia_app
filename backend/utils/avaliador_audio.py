# File: backend/utils/avaliador_audio.py

import os
from openai import OpenAI

# Carrega a chave da variável de ambiente, não o valor literal
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise RuntimeError("Missing OPENAI_API_KEY environment variable")

client = OpenAI(api_key=api_key)

def avaliar_leitura_voz(audio_path: str) -> dict:
    """
    Avalia a qualidade da leitura em voz alta de um arquivo de áudio.
    Retorna um dicionário com pontuação e feedback.
    """
    transcription = client.audio.transcriptions.create(
        file=open(audio_path, "rb"),
        model="whisper-1"
    )

    feedback = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Você é um avaliador de leitura em voz alta."},
            {"role": "user", "content": f"Transcrição: {transcription.text}. Forneça feedback sobre pronúncia e fluidez."}
        ]
    )

    return {
        "transcription": transcription.text,
        "feedback": feedback.choices[0].message.content
    }

