# File: backend/schemas.py

from pydantic import BaseModel, ConfigDict
from typing import List, Optional, Dict
from datetime import date, datetime

# 🔹 Aluno
class AlunoCreate(BaseModel):
    nome: str
    email: str
    senha: str
    foto_url: Optional[str] = None
    model_config = ConfigDict(from_attributes=True)

class AlunoOut(BaseModel):
    id: int
    nome: str
    email: str
    foto_url: Optional[str]
    model_config = ConfigDict(from_attributes=True)

# 🔹 Login
class LoginData(BaseModel):
    email: str
    senha: str
    model_config = ConfigDict(from_attributes=True)

class LoginResponse(BaseModel):
    message: str
    aluno_id: int
    nome: str
    token: str
    model_config = ConfigDict(from_attributes=True)

# 🔹 Perguntas (atualizado)
class PerguntaCreate(BaseModel):
    materia: str
    enunciado: str
    resposta_correta: str
    dificuldade: Optional[str] = "media"
    model_config = ConfigDict(from_attributes=True)

class PerguntaOut(BaseModel):
    id: int
    materia: str
    enunciado: str
    resposta_correta: str
    dificuldade: Optional[str]
    model_config = ConfigDict(from_attributes=True)

# 🔹 Provas
class QuestaoProvaCreate(BaseModel):
    pergunta_id: int

class RespostaProvaCreate(BaseModel):
    pergunta_id: int
    resposta: str

class ProvaCreate(BaseModel):
    aluno_id: int
    materia: str
    questoes: List[QuestaoProvaCreate]

class ProvaOut(BaseModel):
    id: int
    aluno_id: int
    materia: str
    model_config = ConfigDict(from_attributes=True)

class ResultadoProvaOut(BaseModel):
    prova_id: int
    nota: float

# 🔹 Relatório
class RelatorioMensalOut(BaseModel):
    aluno_id: int
    nome: str
    email: str
    foto_url: Optional[str]
    media_geral: float
    mensagem_motivacional: str

# 🔹 Notas
class NotaMensalOut(BaseModel):
    id: int
    aluno_id: int
    materia: str
    nota: float
    mes: str
    model_config = ConfigDict(from_attributes=True)

class NotaMensalCreate(BaseModel):
    aluno_id: int
    materia: str
    nota: float
    mes: str

# 🔹 Recompensas
class RecompensaOut(BaseModel):
    id: int
    aluno_id: int
    tipo: str
    descricao: str
    data: str
    model_config = ConfigDict(from_attributes=True)

class RecompensaCreate(BaseModel):
    aluno_id: int
    tipo: str
    descricao: str
    data: str

# 🔹 Medalhas
class MedalhaOut(BaseModel):
    id: int
    titulo: str
    descricao: str
    data_conquista: str
    model_config = ConfigDict(from_attributes=True)

class MedalhasDoAluno(BaseModel):
    aluno_id: int
    nome: str
    medalhas: List[MedalhaOut]

# 🔹 Trilha de Aprendizado
class TrilhaAprendizadoOut(BaseModel):
    id: int
    aluno_id: int
    titulo: str
    descricao: Optional[str] = None
    habilidade: str
    status: str
    data_criacao: Optional[date]
    model_config = ConfigDict(from_attributes=True)

class TrilhaAprendizadoCreate(BaseModel):
    aluno_id: int
    titulo: str
    descricao: Optional[str] = None
    habilidade: str

# 🔹 Escrita Criativa
class EscritaCriativaOut(BaseModel):
    id: int
    aluno_id: int
    tema: str
    texto: str
    feedback: Optional[str] = None
    data_envio: Optional[date]
    model_config = ConfigDict(from_attributes=True)

class EscritaCriativaCreate(BaseModel):
    aluno_id: int
    tema: str
    texto: str

# 🔹 Explicação com IA
class ExplicacaoRequest(BaseModel):
    pergunta: str

class ExplicacaoResponse(BaseModel):
    resposta: str

# 🔹 Estudo Diário
class EstudoDiarioIn(BaseModel):
    aluno_id: int

# 🔹 Mural de Conquistas
class ConquistaOut(BaseModel):
    id: int
    aluno_id: int
    titulo: str
    descricao: str
    data_conquista: date
    model_config = ConfigDict(from_attributes=True)

class ConquistaCreate(BaseModel):
    aluno_id: int
    titulo: str
    descricao: str
    data_conquista: date
    model_config = ConfigDict(from_attributes=True)

# 🔹 Prova Gerada
class QuestaoResposta(BaseModel):
    pergunta_id: int
    resposta: str

class GerarProvaRequest(BaseModel):
    aluno_id: int
    materia: str
    questoes: List[QuestaoResposta]

# 🔹 Respostas do Aluno
class RespostaAlunoSchema(BaseModel):
    aluno_id: int
    pergunta_id: int
    resposta: str
    correta: str
    materia: str

# 🔹 Progresso (Histórico de Desempenho)
class ProgressoCreate(BaseModel):
    aluno_id: int
    materia: str
    acertos: int
    erros: int

class ProgressoOut(BaseModel):
    id: int
    aluno_id: int
    materia: str
    acertos: int
    erros: int
    data: date
    model_config = ConfigDict(from_attributes=True)

# 🔹 Motivação
class MotivacaoOut(BaseModel):
    aluno_id: int
    mensagem: str
    model_config = ConfigDict(from_attributes=True)

# 🔹 Quiz Lúdico
class QuizRequest(BaseModel):
    materia: str
    assunto: Optional[str] = None
    quantidade: Optional[int] = 5

class PerguntaQuiz(BaseModel):
    enunciado: str
    opcoes: List[str]
    resposta_correta: Optional[str] = None

class QuizResponse(BaseModel):
    perguntas: List[PerguntaQuiz]

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

# 🔹 Resumo Orientado
class ResumoRequest(BaseModel):
    aluno_id: int
    texto: str
    estilo: Optional[str] = "bullet points"

class ResumoOut(BaseModel):
    id: int
    aluno_id: int
    conteudo: str
    data: datetime
    model_config = ConfigDict(from_attributes=True)






 
























    




































