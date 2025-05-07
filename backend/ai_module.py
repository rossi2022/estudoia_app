import openai
import os
from dotenv import load_dotenv
from typing import List, Optional
import json
from pydantic import BaseModel, ConfigDict

# 🔹 Carrega variáveis do .env com caminho explícito
dotenv_path = os.path.join(os.path.dirname(__file__), "..", ".env")
load_dotenv(dotenv_path)

# 🔹 Define a chave da OpenAI
openai.api_key = os.getenv("OPENAI_API_KEY")

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

# 🔹 IA para gerar perguntas fixas por matéria
def gerar_perguntas_por_materia(materia: str, dificuldade: str = "media") -> List[str]:
    perguntas = {
        "Matemática": {
            "facil": ["Quanto é 2 + 2?", "Qual é o dobro de 5?"],
            "media": ["Resolva: 3x - 2 = 7", "Qual é a área de um quadrado de lado 4?"],
            "dificil": ["Derive a função f(x) = 3x² + 2x", "Resolva a equação log(x) + log(2) = 1"]
        }
    }
    return perguntas.get(materia, {}).get(dificuldade, ["Pergunta não encontrada para essa matéria."])

# 🔹 Função para selecionar trecho literário
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

# 🔹 Função para gerar mensagens motivacionais
def gerar_mensagem_motivacional(resumo: str) -> str:
    try:
        resposta = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Você é um coach motivacional que incentiva alunos com base no desempenho escolar."},
                {"role": "user", "content": f"Com base neste desempenho:\n{resumo}\nGere uma mensagem motivacional curta para o aluno."}
            ],
            max_tokens=100,
            temperature=0.7
        )
        return resposta.choices[0].message.content.strip()
    except Exception as e:
        return f"Erro ao gerar mensagem motivacional: {str(e)}"

# 🔹 Função para gerar resumos orientados
def gerar_resumo(texto: str, estilo: str) -> str:
    try:
        prompt = (
            f"Você é um tutor de ensino médio. "
            f"Pegue este texto e crie um resumo em formato {estilo}, "
            "destacando palavras-chave e levantando 2 perguntas de reflexão no final."
        )
        resposta = openai.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": texto}
            ],
            temperature=0.5
        )
        return resposta.choices[0].message.content.strip()
    except Exception as e:
        return f"Erro ao gerar resumo: {str(e)}"

# 🔹 Função para gerar quizzes lúdicos
def gerar_quiz(materia: str, assunto: Optional[str], quantidade: int) -> List[dict]:
    topo = f"Crie {quantidade} perguntas de múltipla escolha sobre {materia}"
    if assunto:
        topo += f" (assunto específico: {assunto})"
    prompt = (
        f"{topo}, adequadas para alunos do ensino médio. "
        "Para cada pergunta, forneça 4 opções e marque qual é a correta."
    )
    try:
        resp = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Você gera quizzes educativos."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.8
        )
        texto = resp.choices[0].message.content.strip()
        return parse_quiz(texto)
    except Exception as e:
        return [{"error": str(e)}]

# 🔹 Função auxiliar para parsear o quiz
def parse_quiz(texto: str) -> List[dict]:
    try:
        return json.loads(texto)
    except json.JSONDecodeError:
        blocos = texto.split("\n\n")
        perguntas = []
        for bloco in blocos:
            linhas = [l.strip() for l in bloco.split("\n") if l.strip()]
            if not linhas:
                continue
            enunciado = linhas[0]
            opcoes = linhas[1:5]
            perguntas.append({"enunciado": enunciado, "opcoes": opcoes, "resposta_correta": opcoes[0] if opcoes else None})
        return perguntas

# 🔹 Linha do Tempo (História)
class TimelineRequest(BaseModel):
    periodo: str
    eventos: Optional[int] = 5

class EventoTimeline(BaseModel):
    data: str
    evento: str

class TimelineResponse(BaseModel):
    periodo: str
    eventos: List[EventoTimeline]
    model_config = ConfigDict(from_attributes=True)

# 🔹 Função para gerar linha do tempo histórica
def gerar_timeline(periodo: str, eventos: int) -> List[dict]:
    exemplos = {
        "Revolução Francesa": [
            {"data": "1789-07-14", "evento": "Queda da Bastilha"},
            {"data": "1789-08-26", "evento": "Declaração dos Direitos do Homem"},
            {"data": "1791-09-03", "evento": "Primeira Constituição Francesa"},
            {"data": "1793-01-21", "evento": "Execução de Luís XVI"},
            {"data": "1799-11-09", "evento": "Golpe de 18 de Brumário"}
        ]
    }
    return exemplos.get(periodo, [])[:eventos]

# 🔹 Função para gerar agenda de estudos inteligente
def gerar_agenda_estudos(resumo: str) -> str:
    try:
        prompt = (
            "Você é um orientador educacional. Com base nesse desempenho:\n"
            f"{resumo}\n\nMonte uma agenda de estudos para o aluno com foco nas matérias com mais dificuldade. "
            "Inclua pausas, tempo para leitura, caligrafia e revisão."
        )
        resposta = openai.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "Você monta agendas de estudo inteligentes para alunos do ensino médio."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=500
        )
        return resposta.choices[0].message.content.strip()
    except Exception as e:
        return f"Erro ao gerar agenda de estudos: {str(e)}"














