# backend/utils/avaliador_audio.py

import os
from dotenv import load_dotenv
from openai import OpenAI

# 🔐 Carrega a chave da OpenAI do .env
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# ✅ Função compatível com import: avaliar_leitura_voz
def avaliar_leitura_voz(caminho_audio: str) -> str:
    try:
        # 📤 Lê o conteúdo do arquivo em bytes
        with open(caminho_audio, "rb") as f:
            audio_bytes = f.read()

        # ✅ Transcreve com Whisper
        transcript = client.audio.transcriptions.create(
            model="whisper-1",
            file=audio_bytes,
            response_format="text"
        )

        texto_transcrito = transcript.strip()

        # 🧠 Gera avaliação com IA
        prompt = (
            f"O seguinte texto foi lido por um aluno:\n\n\"{texto_transcrito}\"\n\n"
            "Avalie a fluência, entonação e clareza da leitura como se fosse um professor de português. "
            "Seja gentil e motivador. Dê uma nota de 0 a 10 e um comentário construtivo."
        )

        resposta = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Você é um avaliador de leitura em voz alta para alunos do ensino médio."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=300
        )

        return resposta.choices[0].message.content.strip()

    except Exception as e:
        return f"Erro ao avaliar áudio: {str(e)}"

