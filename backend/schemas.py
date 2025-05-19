# File: backend/schemas.py

from pydantic import BaseModel, ConfigDict, Field
from typing import List, Optional
from datetime import date, datetime

# Common BaseModel config for ORM
ORM_MODEL_CONFIG = ConfigDict(from_attributes=True)

# 🔹 Aluno
class AlunoCreate(BaseModel):
    nome: str
    email: str
    senha: str
    foto_url: Optional[str] = None

    model_config = ORM_MODEL_CONFIG

class AlunoOut(BaseModel):
    id: int
    nome: str
    email: str
    foto_url: Optional[str]

    model_config = ORM_MODEL_CONFIG

# 🔹 Login
class LoginData(BaseModel):
    email: str
    senha: str

    model_config = ORM_MODEL_CONFIG

class LoginResponse(BaseModel):
    message: str
    aluno_id: int
    nome: str
    token: str

    model_config = ORM_MODEL_CONFIG

# 🔹 Perguntas
class PerguntaCreate(BaseModel):
    materia: str
    enunciado: str = Field(..., alias="pergunta")
    resposta_correta: str
    dificuldade: Optional[str] = "media"

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

class PerguntaOut(BaseModel):
    id: int
    materia: str
    enunciado: str = Field(..., alias="pergunta")
    resposta_correta: str
    dificuldade: Optional[str]

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

# 🔹 Provas
class QuestaoProvaCreate(BaseModel):
    pergunta_id: int
    model_config = ORM_MODEL_CONFIG

class RespostaProvaCreate(BaseModel):
    prova_id: int
    pergunta_id: int
    resposta: str
    model_config = ORM_MODEL_CONFIG

class ProvaCreate(BaseModel):
    aluno_id: int
    materia: str
    questoes: List[QuestaoProvaCreate]
    model_config = ORM_MODEL_CONFIG

class ProvaOut(BaseModel):
    id: int
    aluno_id: int
    conteudo: Optional[str] = None
    data_prova: Optional[datetime] = None
    nota_final: Optional[float] = None

    model_config = ORM_MODEL_CONFIG

class ResultadoProvaOut(BaseModel):
    prova_id: int
    nota: float

    model_config = ORM_MODEL_CONFIG

# 🔹 Relatório Mensal
class RelatorioMensalOut(BaseModel):
    aluno_id: int
    nome: str
    email: str
    foto_url: Optional[str]
    media_geral: float
    mensagem_motivacional: str

    model_config = ORM_MODEL_CONFIG

# 🔹 Notas Mensais
class NotaMensalCreate(BaseModel):
    aluno_id: int
    materia: str
    nota: float
    mes: str
    ano: int

    model_config = ORM_MODEL_CONFIG

class NotaMensalOut(BaseModel):
    id: int
    aluno_id: int
    materia: str
    nota: float
    mes: str
    ano: int

    model_config = ORM_MODEL_CONFIG

# 🔹 Recompensas
class RecompensaCreate(BaseModel):
    aluno_id: int
    tipo: str
    descricao: str
    data: str

    model_config = ORM_MODEL_CONFIG

class RecompensaOut(BaseModel):
    id: int
    aluno_id: int
    tipo: str
    descricao: str
    data: str

    model_config = ORM_MODEL_CONFIG

# 🔹 Medalhas
class MedalhaOut(BaseModel):
    id: int
    titulo: str
    descricao: str
    data_conquista: date

    model_config = ORM_MODEL_CONFIG

class MedalhasDoAluno(BaseModel):
    aluno_id: int
    nome: str
    medalhas: List[MedalhaOut]

    model_config = ORM_MODEL_CONFIG

# 🔹 Trilhas de Aprendizado
class TrilhaAprendizadoCreate(BaseModel):
    aluno_id: int
    titulo: str
    descricao: Optional[str] = None
    habilidade: str

    model_config = ORM_MODEL_CONFIG

class TrilhaAprendizadoOut(BaseModel):
    id: int
    aluno_id: int
    titulo: str
    descricao: Optional[str]
    habilidade: str
    status: str
    data_criacao: Optional[date]

    model_config = ORM_MODEL_CONFIG

# 🔹 Escrita Criativa
class EscritaCriativaCreate(BaseModel):
    aluno_id: int
    tema: str
    texto: str

    model_config = ORM_MODEL_CONFIG

class EscritaCriativaOut(BaseModel):
    id: int
    aluno_id: int
    tema: str
    texto: str
    feedback: Optional[str]
    data_envio: Optional[date]

    model_config = ORM_MODEL_CONFIG

# 🔹 Estudo Diário
class EstudoDiarioIn(BaseModel):
    aluno_id: int

    model_config = ORM_MODEL_CONFIG

class CheckinOut(BaseModel):
    aluno_id: int
    data: date

    model_config = ORM_MODEL_CONFIG

# 🔹 Conquistas
class ConquistaCreate(BaseModel):
    aluno_id: int
    titulo: str
    descricao: str
    data_conquista: date

    model_config = ORM_MODEL_CONFIG

class ConquistaOut(BaseModel):
    id: int
    aluno_id: int
    titulo: str
    descricao: str
    data_conquista: date

    model_config = ORM_MODEL_CONFIG

# 🔹 Respostas Aluno
class RespostaAlunoSchema(BaseModel):
    aluno_id: int
    pergunta_id: int
    resposta: str
    correta: str
    materia: str

    model_config = ORM_MODEL_CONFIG

# 🔹 Progresso
class ProgressoCreate(BaseModel):
    aluno_id: int
    materia: str
    acertos: int
    erros: int

    model_config = ORM_MODEL_CONFIG

class ProgressoOut(BaseModel):
    id: int
    aluno_id: int
    materia: str
    acertos: int
    erros: int
    data: date

    model_config = ORM_MODEL_CONFIG

# 🔹 Motivacao
class MotivacaoOut(BaseModel):
    aluno_id: int
    mensagem: str

    model_config = ORM_MODEL_CONFIG

# 🔹 Quiz
class QuizRequest(BaseModel):
    materia: str
    assunto: Optional[str] = None
    quantidade: Optional[int] = 5

    model_config = ORM_MODEL_CONFIG

class PerguntaQuiz(BaseModel):
    enunciado: str
    opcoes: List[str]
    resposta_correta: Optional[str]

    model_config = ORM_MODEL_CONFIG

class QuizResponse(BaseModel):
    perguntas: List[PerguntaQuiz]

    model_config = ORM_MODEL_CONFIG

# 🔹 Timeline
class TimelineRequest(BaseModel):
    periodo: str
    eventos: Optional[int] = 5

    model_config = ORM_MODEL_CONFIG

class EventoTimeline(BaseModel):
    data: str
    evento: str

    model_config = ORM_MODEL_CONFIG

class TimelineResponse(BaseModel):
    periodo: str
    eventos: List[EventoTimeline]

    model_config = ORM_MODEL_CONFIG

# 🔹 Resumos
class ResumoRequest(BaseModel):
    aluno_id: int
    texto: str
    estilo: Optional[str] = "bullet points"

    model_config = ORM_MODEL_CONFIG

class ResumoOut(BaseModel):
    id: int
    aluno_id: int
    conteudo: str
    data: datetime

    model_config = ORM_MODEL_CONFIG

# 🔹 Agenda
class AgendaOut(BaseModel):
    data_gerada: date
    sugestao: str

    model_config = ORM_MODEL_CONFIG

# 🔹 Materias
class MateriaOut(BaseModel):
    nome: str
    apostila_url: Optional[str]

    model_config = ORM_MODEL_CONFIG

# 🔹 Provas Personalizadas
class ProvaPersonalizadaCreate(BaseModel):
    professor_id: int
    titulo: str
    descricao: str
    data_entrega: datetime

    model_config = ORM_MODEL_CONFIG

class ProvaPersonalizadaOut(BaseModel):
    id: int
    professor_id: int
    titulo: str
    descricao: str
    data_criacao: datetime
    data_entrega: datetime

    model_config = ORM_MODEL_CONFIG

# 🔹 Professor
class ProfessorLogin(BaseModel):
    email: str
    senha: str

    model_config = ORM_MODEL_CONFIG

class ProfessorOut(BaseModel):
    id: int
    nome: str
    email: str
    foto_url: Optional[str]

    model_config = ORM_MODEL_CONFIG

# 🔹 Trabalhos
class TrabalhoBase(BaseModel):
    titulo: str
    tema: Optional[str]
    prazo_entrega: Optional[date]

    model_config = ORM_MODEL_CONFIG

class TrabalhoCreate(TrabalhoBase):
    professor_id: int

class TrabalhoOut(TrabalhoBase):
    id: int
    professor_id: int
    criado_em: datetime

    model_config = ORM_MODEL_CONFIG

# 🔹 Entregas de Trabalho
class EntregaCreate(BaseModel):
    trabalho_id: int
    aluno_id: int
    resposta: str

    model_config = ORM_MODEL_CONFIG

class EntregaOut(BaseModel):
    id: int
    trabalho_id: int
    aluno_id: int
    resposta: str
    data_entrega: datetime

    model_config = ORM_MODEL_CONFIG















    




































