# File: backend/openai_api.py

import os
from dotenv import load_dotenv
import openai
from typing import List

# ─────────── Carrega variáveis do `.env` ───────────
dotenv_path = os.path.join(os.path.dirname(__file__), "..", ".env")
load_dotenv(dotenv_path)

# ─────────── Define a chave da OpenAI corretamente ───────────
openai.api_key = os.getenv("OPENAI_API_KEY")
if not openai.api_key:
    raise RuntimeError("OPENAI_API_KEY não definida. Verifique seu .env ou variável de ambiente.")

# ─────────── Função para gerar explicações com IA ───────────
def gerar_explicacao(pergunta: str) -> str:
    try:
        resposta = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": "Você é um professor que explica de forma clara e objetiva para estudantes do ensino médio."
                },
                {"role": "user", "content": f"Explique de forma clara: {pergunta}"}
            ],
            max_tokens=300,
            temperature=0.7
        )
        return resposta.choices[0].message.content.strip()
    except Exception as e:
        return f"Erro ao gerar explicação: {e}"

# ─────────── Função para gerar perguntas com base em matéria e nível ───────────
def gerar_perguntas(materia: str, dificuldade: str = "fácil") -> List[str]:
    prompt = (
        f"Crie 3 perguntas de múltipla escolha sobre {materia} "
        f"com nível de dificuldade {dificuldade}, adequadas para ensino médio."
    )
    try:
        resposta = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Você é um gerador de perguntas escolares."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=500,
            temperature=0.8
        )
        texto = resposta.choices[0].message.content.strip()
        # Quebra em blocos de duas quebras de linha ou em linhas simples
        if "\n\n" in texto:
            itens = texto.split("\n\n")
        else:
            itens = texto.split("\n")
        return [item.strip() for item in itens if item.strip()]
    except Exception as e:
        return [f"Erro ao gerar perguntas: {e}"]

# ─────────── Perguntas definidas estaticamente por matéria ───────────
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
            "dificil": ["Explique a função sintática do termo destacado em: 'João, que é médico, chegou cedo.'"]
        },
        "História": {
            "facil": ["Quem descobriu o Brasil?", "Em que ano foi proclamada a independência do Brasil?"],
            "media": ["Explique a importância da Revolução Francesa.", "O que foi a Ditadura Militar no Brasil?"],
            "dificil": ["Compare o feudalismo europeu com o sistema colonial brasileiro."]
        },
        "Biologia": {
            "facil": ["O que é fotossíntese?", "Qual órgão é responsável pela respiração?"],
            "media": ["Explique a função dos ribossomos.", "O que são células-tronco?"],
            "dificil": ["Explique a replicação do DNA passo a passo."]
        }
    }
    return perguntas.get(materia, {}).get(dificuldade, ["Pergunta não encontrada para essa matéria."])

# ─────────── IA para selecionar trecho de literatura ───────────
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
    return {"autor": autor, "trecho": trecho, "perguntas": perguntas}

# ─────────── Perguntas personalizadas com base no desempenho ───────────
def gerar_perguntas_personalizadas(dados_desempenho: dict) -> List[str]:
    prompt = (
        f"Com base no seguinte desempenho do aluno, gere 3 perguntas de reforço:\n"
        f"{dados_desempenho}\n"
        "As perguntas devem ser objetivas, variadas e focadas nas dificuldades apresentadas."
    )
    try:
        resposta = openai.ChatCompletion.create(
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
        return [f"Erro ao gerar perguntas personalizadas: {e}"]

# ─────────── Mensagem motivacional personalizada ───────────
def gerar_mensagem_motivacional(dados_desempenho: dict) -> str:
    prompt = (
        f"Com base no desempenho a seguir, gere uma mensagem motivacional personalizada "
        f"para o aluno:\n\n{dados_desempenho}\n\n"
        "A mensagem deve ser positiva, curta (máximo 2 frases), encorajadora e motivadora."
    )
    try:
        resposta = openai.ChatCompletion.create(
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
        return f"Não foi possível gerar a mensagem motivacional: {e}"












