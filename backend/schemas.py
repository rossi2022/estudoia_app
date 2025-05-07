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

# 🔹 Perguntas
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
    model_config = ConfigDict(from_attributes=True)

class RespostaProvaCreate(BaseModel):
    prova_id: int
    pergunta_id: int
    resposta: str
    model_config = ConfigDict(from_attributes=True)

class ProvaCreate(BaseModel):
    aluno_id: int
    materia: str
    questoes: List[QuestaoProvaCreate]
    model_config = ConfigDict(from_attributes=True)

class ProvaOut(BaseModel):
    id: int
    aluno_id: int
    conteudo: Optional[str] = None
    data_prova: Optional[datetime] = None
    nota_final: Optional[float] = None
    model_config = ConfigDict(from_attributes=True)

class ResultadoProvaOut(BaseModel):
    prova_id: int
    nota: float
    model_config = ConfigDict(from_attributes=True)

# 🔹 Prova Gerada
class QuestaoResposta(BaseModel):
    pergunta_id: int
    resposta: str
    model_config = ConfigDict(from_attributes=True)

class GerarProvaRequest(BaseModel):
    aluno_id: int
    materia: str
    model_config = ConfigDict(from_attributes=True)

# 🔹 Relatório
class RelatorioMensalOut(BaseModel):
    aluno_id: int
    nome: str
    email: str
    foto_url: Optional[str]
    media_geral: float
    mensagem_motivacional: str
    model_config = ConfigDict(from_attributes=True)

# 🔹 Notas
class NotaMensalCreate(BaseModel):
    aluno_id: int
    materia: str
    nota: float
    mes: str
    ano: int
    model_config = ConfigDict(from_attributes=True)

# ❗ Este modelo deve estar em models.py — mantido aqui apenas conforme seu pedido
# class NotaMensal(Base):
#     __tablename__ = "notas_mensais"
#     id = Column(Integer, primary_key=True)
#     aluno_id = Column(Integer, ForeignKey("alunos.id"))
#     materia = Column(String)
#     nota = Column(Float)
#     mes = Column(String)
#     ano = Column(Integer)

class NotaMensalOut(BaseModel):
    id: int
    aluno_id: int
    materia: str
    nota: float
    mes: str
    ano: int
    model_config = ConfigDict(from_attributes=True)

# 🔹 Recompensas
class RecompensaCreate(BaseModel):
    aluno_id: int
    tipo: str
    descricao: str
    data: str
    model_config = ConfigDict(from_attributes=True)

class RecompensaOut(BaseModel):
    id: int
    aluno_id: int
    tipo: str
    descricao: str
    data: str
    model_config = ConfigDict(from_attributes=True)

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
    model_config = ConfigDict(from_attributes=True)

# 🔹 Trilha de Aprendizado
class TrilhaAprendizadoCreate(BaseModel):
    aluno_id: int
    titulo: str
    descricao: Optional[str] = None
    habilidade: str
    model_config = ConfigDict(from_attributes=True)

class TrilhaAprendizadoOut(BaseModel):
    id: int
    aluno_id: int
    titulo: str
    descricao: Optional[str] = None
    habilidade: str
    status: str
    data_criacao: Optional[date]
    model_config = ConfigDict(from_attributes=True)

class TrilhaIn(BaseModel):
    aluno_id: int
    titulo: str
    descricao: str
    habilidade: str

class TrilhaOut(BaseModel):
    id: int
    aluno_id: int
    titulo: str
    descricao: str
    habilidade: str
    status: str
    model_config = ConfigDict(from_attributes=True)

# 🔹 Escrita Criativa
class EscritaCriativaCreate(BaseModel):
    aluno_id: int
    tema: str
    texto: str
    model_config = ConfigDict(from_attributes=True)

class EscritaCriativaOut(BaseModel):
    id: int
    aluno_id: int
    tema: str
    texto: str
    feedback: Optional[str] = None
    data_envio: Optional[date]
    model_config = ConfigDict(from_attributes=True)

# 🔹 Explicação com IA
class ExplicacaoRequest(BaseModel):
    pergunta: str
    model_config = ConfigDict(from_attributes=True)

class ExplicacaoResponse(BaseModel):
    resposta: str
    model_config = ConfigDict(from_attributes=True)

# 🔹 Estudo Diário
class EstudoDiarioIn(BaseModel):
    aluno_id: int
    model_config = ConfigDict(from_attributes=True)

class CheckinOut(BaseModel):
    aluno_id: int
    data: date
    model_config = ConfigDict(from_attributes=True)

# 🔹 Mural de Conquistas
class ConquistaCreate(BaseModel):
    aluno_id: int
    titulo: str
    descricao: str
    data_conquista: date
    model_config = ConfigDict(from_attributes=True)

class ConquistaOut(BaseModel):
    id: int
    aluno_id: int
    titulo: str
    descricao: str
    data_conquista: date
    model_config = ConfigDict(from_attributes=True)

# 🔹 Respostas do Aluno
class RespostaAlunoSchema(BaseModel):
    aluno_id: int
    pergunta_id: int
    resposta: str
    correta: str
    materia: str
    model_config = ConfigDict(from_attributes=True)

# 🔹 Progresso
class ProgressoCreate(BaseModel):
    aluno_id: int
    materia: str
    acertos: int
    erros: int
    model_config = ConfigDict(from_attributes=True)

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

# 🔹 Quiz
class QuizRequest(BaseModel):
    materia: str
    assunto: Optional[str] = None
    quantidade: Optional[int] = 5
    model_config = ConfigDict(from_attributes=True)

class PerguntaQuiz(BaseModel):
    enunciado: str
    opcoes: List[str]
    resposta_correta: Optional[str] = None
    model_config = ConfigDict(from_attributes=True)

class QuizResponse(BaseModel):
    perguntas: List[PerguntaQuiz]
    model_config = ConfigDict(from_attributes=True)

# 🔹 Linha do Tempo
class TimelineRequest(BaseModel):
    periodo: str
    eventos: Optional[int] = 5
    model_config = ConfigDict(from_attributes=True)

class EventoTimeline(BaseModel):
    data: str
    evento: str
    model_config = ConfigDict(from_attributes=True)

class TimelineResponse(BaseModel):
    periodo: str
    eventos: List[EventoTimeline]
    model_config = ConfigDict(from_attributes=True)

# 🔹 Resumos
class ResumoRequest(BaseModel):
    aluno_id: int
    texto: str
    estilo: Optional[str] = "bullet points"
    model_config = ConfigDict(from_attributes=True)

class ResumoOut(BaseModel):
    id: int
    aluno_id: int
    conteudo: str
    data: datetime
    model_config = ConfigDict(from_attributes=True)

# 🔹 Agenda
class AgendaOut(BaseModel):
    data_gerada: date
    sugestao: str
    model_config = ConfigDict(from_attributes=True)

# 🔹 Matérias (fixas)
class MateriaOut(BaseModel):
    nome: str
    model_config = ConfigDict(from_attributes=True)

# 🔹 Provas Personalizadas
class ProvaPersonalizadaCreate(BaseModel):
    professor_id: int
    titulo: str
    descricao: str
    data_entrega: datetime
    model_config = ConfigDict(from_attributes=True)

class ProvaPersonalizadaOut(BaseModel):
    id: int
    professor_id: int
    titulo: str
    descricao: str
    data_criacao: datetime
    data_entrega: datetime
    model_config = ConfigDict(from_attributes=True)

# 🔹 Professor
class ProfessorLogin(BaseModel):
    email: str
    senha: str

class ProfessorOut(BaseModel):
    id: int
    nome: str
    email: str

    class Config:
        orm_mode = True



















    




































