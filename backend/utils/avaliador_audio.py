import os
from dotenv import load_dotenv
from openai import OpenAI
import base64

# 🔐 Carrega a chave da OpenAI do .env
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# 🔍 Função que avalia a fluência e entonação a partir de um arquivo de áudio
def avaliar_leitura_por_audio(caminho_audio: str) -> str:
    try:
        # 📤 Lê o conteúdo do arquivo em bytes
        with open(caminho_audio, "rb") as f:
            audio_bytes = f.read()

        # ✅ Envia para o Whisper (modelo de transcrição)
        transcript = client.audio.transcriptions.create(
            model="whisper-1",
            file=audio_bytes,
            response_format="text"
        )

        texto_transcrito = transcript.strip()

        # 🧠 Envia para a IA avaliar a fluência e entonação do texto lido
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
