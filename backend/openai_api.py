# backend/openai_api.py

import openai
import os
from dotenv import load_dotenv
from typing import List

# 🔹 Carrega variáveis do .env com caminho explícito
dotenv_path = os.path.join(os.path.dirname(__file__), "..", ".env")
load_dotenv(dotenv_path)

# 🔹 Define a chave da OpenAI corretamente
openai.api_key = os.getenv("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")  # ✅ Correto

# 🔹 Função para gerar explicações com IA
def gerar_explicacao(pergunta: str) -> str:
    try:
        resposta = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Você é um professor que explica de forma clara e objetiva para estudantes do ensino médio."},
                {"role": "user", "content": f"Explique de forma clara: {pergunta}"}
            ],
            max_tokens=300,
            temperature=0.7
        )
        return resposta.choices[0].message.content.strip()
    except Exception as e:
        return f"Erro ao gerar explicação: {str(e)}"

# 🔹 Função para gerar perguntas com base em uma matéria e nível
def gerar_perguntas(materia: str, dificuldade: str = "fácil") -> List[str]:
    prompt = f"Crie 3 perguntas de múltipla escolha sobre {materia} com nível de dificuldade {dificuldade}, adequadas para ensino médio."
    try:
        resposta = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Você é um gerador de perguntas escolares."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=500,
            temperature=0.8
        )
        texto = resposta.choices[0].message.content.strip()
        perguntas = texto.split("\n\n") if "\n\n" in texto else texto.split("\n")
        return [p.strip() for p in perguntas if p.strip()]
    except Exception as e:
        return [f"Erro ao gerar perguntas: {str(e)}"]

# 🔹 IA para gerar perguntas com base no conteúdo fixo
def gerar_perguntas_por_materia(materia: str, dificuldade: str = "media") -> List[str]:
    perguntas = {
        "Matemática": {
            "facil": ["Quanto é 2 + 2?", "Qual é o dobro de 5?"],
            "media": ["Resolva: 3x - 2 = 7", "Qual é a área de um quadrado de lado 4?"],
            "dificil": ["Derive a função f(x) = 3x² + 2x", "Resolva a equação log(x) + log(2) = 1"]
        },
        "Português": {
            "facil": ["Qual é o antônimo de 'alegre'?", "Complete: O sol ____ brilhando."],
            "media": ["O que é um adjetivo?", "Identifique o sujeito na frase: 'Os alunos estudaram bastante.'"],
            "dificil": ["Explique a função sintática do termo destacado na frase: 'João, que é médico, chegou cedo.'"]
        },
        "História": {
            "facil": ["Quem descobriu o Brasil?", "Em que ano foi proclamada a independência do Brasil?"],
            "media": ["Explique a importância da Revolução Francesa.", "O que foi o período da Ditadura Militar no Brasil?"],
            "dificil": ["Compare o feudalismo europeu com o sistema colonial brasileiro."]
        },
        "Biologia": {
            "facil": ["O que é fotossíntese?", "Qual órgão é responsável pela respiração?"],
            "media": ["Explique a função dos ribossomos.", "O que são células-tronco?"],
            "dificil": ["Explique a replicação do DNA passo a passo."]
        }
    }
    return perguntas.get(materia, {}).get(dificuldade, ["Pergunta não encontrada para essa matéria."])

# 🔹 IA para trechos de leitura (Literatura)
def selecionar_trecho_literatura() -> dict:
    trecho = (
        "Ninguém escreve para o outro. Escreve-se para preencher o vazio de si mesmo. "
        "Mas quando o outro se reconhece nesse vazio, nasce a literatura."
    )
    autor = "Mia Couto"
    perguntas = [
        "O que o autor quer dizer com 'preencher o vazio de si mesmo'?",
        "Como a literatura conecta o autor e o leitor nesse trecho?",
        "Você concorda com a ideia apresentada? Por quê?",
        "Interprete a frase: 'nasce a literatura'.",
        "Qual é o tom emocional do trecho?"
    ]
    return {
        "autor": autor,
        "trecho": trecho,
        "perguntas": perguntas
    }

# 🔹 IA para perguntas personalizadas com base no desempenho
def gerar_perguntas_personalizadas(dados_desempenho: dict) -> List[str]:
    prompt = f"""
    Com base no seguinte desempenho do aluno, gere 3 perguntas de reforço:
    {dados_desempenho}
    As perguntas devem ser objetivas, variadas e focadas nas dificuldades apresentadas.
    """
    try:
        resposta = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Você é um gerador de perguntas personalizadas para estudo."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=500,
            temperature=0.7
        )
        texto = resposta.choices[0].message.content.strip()
        return [p.strip() for p in texto.split("\n") if p.strip()]
    except Exception as e:
        return [f"Erro ao gerar perguntas personalizadas: {str(e)}"]

# 🔹 IA para mensagem motivacional
def gerar_mensagem_motivacional(dados_desempenho: dict) -> str:
    prompt = f"""
    Com base no desempenho a seguir, gere uma mensagem motivacional personalizada para o aluno:

    {dados_desempenho}

    A mensagem deve ser positiva, curta (máximo 2 frases), encorajadora e motivadora.
    """
    try:
        resposta = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Você é um tutor escolar que motiva alunos com mensagens curtas e positivas."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=150,
            temperature=0.8
        )
        return resposta.choices[0].message.content.strip()
    except Exception as e:
        return f"Não foi possível gerar a mensagem motivacional: {str(e)}"











