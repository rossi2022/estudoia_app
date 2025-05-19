# backend/database/models.py

from datetime import date, datetime
from sqlalchemy import Column, Date, DateTime, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

# Importa o Base único, definido em backend/db.py
from backend.db import Base  

# === daqui em diante, defina só as suas classes que herdam de Base ===
class Aluno(Base):
    __tablename__ = "alunos"
    id        = Column(Integer, primary_key=True, index=True)
    nome      = Column(String, nullable=False)
    email     = Column(String, unique=True, nullable=False)
    senha     = Column(String, nullable=False)
    foto_url  = Column(String, nullable=True)
    meta_estudo = Column(String, nullable=True)

    respostas = relationship("RespostaAluno", back_populates="aluno")
    # … e o restante das relações …

    provas = relationship("Prova", back_populates="aluno", lazy="joined")
    notas = relationship("NotaMensal", back_populates="aluno", lazy="joined")
    recompensas = relationship("Recompensa", back_populates="aluno", lazy="joined")
    medalhas = relationship("Medalha", back_populates="aluno", lazy="joined")
    historico = relationship("HistoricoDesempenho", back_populates="aluno", lazy="joined")
    trilha = relationship("TrilhaAprendizado", back_populates="aluno", lazy="joined")
    trilhas_estudo = relationship("TrilhaDeEstudo", back_populates="aluno", lazy="joined")
    escritas = relationship("EscritaCriativa", back_populates="aluno", lazy="joined")
    estudos_diarios = relationship("EstudoDiario", back_populates="aluno", lazy="joined")
    conquistas = relationship("Conquista", back_populates="aluno", lazy="joined")
    resumos = relationship("Resumo", back_populates="aluno", lazy="joined")
    tarefas_estudo = relationship("TarefaEstudo", back_populates="aluno", lazy="joined")

# ===============================
# 📌 MODELO: Pergunta
# ===============================
class Pergunta(Base):
    __tablename__ = "perguntas"

    id = Column(Integer, primary_key=True, index=True)
    materia = Column(String, nullable=False)
    enunciado = Column(String, nullable=False)
    resposta_correta = Column(String, nullable=False)
    dificuldade = Column(String, nullable=False)

    questoes_prova = relationship("QuestaoProva", back_populates="pergunta")

# ===============================
# 📌 MODELO: RespostaAluno
# ===============================
class RespostaAluno(Base):
    __tablename__ = "respostas_aluno"

    id = Column(Integer, primary_key=True, index=True)
    aluno_id = Column(Integer, ForeignKey("alunos.id"), nullable=False)
    pergunta_id = Column(Integer, ForeignKey("perguntas.id"), nullable=False)
    resposta = Column(String, nullable=False)
    correta = Column(String, nullable=False)
    materia = Column(String, nullable=False)

    aluno = relationship("Aluno", back_populates="respostas")

# ===============================
# 📌 MODELO: NotaMensal
# ===============================
class NotaMensal(Base):
    __tablename__ = "notas_mensais"

    id = Column(Integer, primary_key=True, index=True)
    aluno_id = Column(Integer, ForeignKey("alunos.id"), nullable=False)
    materia = Column(String, nullable=False)
    nota = Column(Float, nullable=False)
    mes = Column(String, nullable=False)
    ano = Column(Integer, default=date.today().year)

    aluno = relationship("Aluno", back_populates="notas")

# ===============================
# 📌 MODELO: Prova + Questões + Respostas
# ===============================
class Prova(Base):
    __tablename__ = "provas"

    id = Column(Integer, primary_key=True, index=True)
    aluno_id = Column(Integer, ForeignKey("alunos.id"), nullable=False)
    nome = Column(String, nullable=False)
    data_prova = Column(DateTime, nullable=False)
    nota_final = Column(Float, nullable=True)
    conteudo = Column(Text, nullable=False)

    aluno = relationship("Aluno", back_populates="provas")
    questoes = relationship("QuestaoProva", back_populates="prova", cascade="all, delete-orphan")
    respostas = relationship("RespostaProva", back_populates="prova", cascade="all, delete-orphan")
    alertas = relationship("AlertaProva", back_populates="prova", cascade="all, delete-orphan")

    @property
    def materia(self):
        if self.questoes and hasattr(self.questoes[0], 'materia'):
            return self.questoes[0].materia
        return "Desconhecida"

class QuestaoProva(Base):
    __tablename__ = "questoes_prova"

    id = Column(Integer, primary_key=True, index=True)
    prova_id = Column(Integer, ForeignKey("provas.id"), nullable=False)
    pergunta_id = Column(Integer, ForeignKey("perguntas.id"), nullable=False)

    prova = relationship("Prova", back_populates="questoes")
    pergunta = relationship("Pergunta", back_populates="questoes_prova")
    respostas = relationship("RespostaProva", back_populates="questao", cascade="all, delete-orphan")

class RespostaProva(Base):
    __tablename__ = "respostas_prova"

    id = Column(Integer, primary_key=True, index=True)
    prova_id = Column(Integer, ForeignKey("provas.id"), nullable=False)
    pergunta_id = Column(Integer, ForeignKey("perguntas.id"), nullable=False)
    questao_id = Column(Integer, ForeignKey("questoes_prova.id"), nullable=True)
    resposta_dada = Column(String, nullable=False)
    correta = Column(String, nullable=False)

    prova = relationship("Prova", back_populates="respostas")
    questao = relationship("QuestaoProva", back_populates="respostas")

# ===============================
# 📌 MODELO: Recompensa
# ===============================
class Recompensa(Base):
    __tablename__ = "recompensas"

    id = Column(Integer, primary_key=True, index=True)
    aluno_id = Column(Integer, ForeignKey("alunos.id"), nullable=False)
    tipo = Column(String, nullable=False)
    descricao = Column(String, nullable=False)
    data = Column(String, nullable=False)

    aluno = relationship("Aluno", back_populates="recompensas")

# ===============================
# 📌 MODELO: Medalha
# ===============================
class Medalha(Base):
    __tablename__ = "medalhas"

    id = Column(Integer, primary_key=True, index=True)
    aluno_id = Column(Integer, ForeignKey("alunos.id"), nullable=False)
    titulo = Column(String, nullable=False)
    descricao = Column(String, nullable=False)
    data_conquista = Column(String, nullable=False)

    aluno = relationship("Aluno", back_populates="medalhas")

# ===============================
# 📌 MODELO: Histórico de Desempenho
# ===============================
class HistoricoDesempenho(Base):
    __tablename__ = "historico_desempenho"

    id = Column(Integer, primary_key=True, index=True)
    aluno_id = Column(Integer, ForeignKey("alunos.id"), nullable=False)
    materia = Column(String, nullable=False)
    acertos = Column(Integer, default=0)
    erros = Column(Integer, default=0)
    data = Column(Date, default=date.today)

    aluno = relationship("Aluno", back_populates="historico")

# ===============================
# 📌 MODELO: Trilha de Aprendizado
# ===============================
class TrilhaAprendizado(Base):
    __tablename__ = "trilhas_aprendizado"

    id = Column(Integer, primary_key=True, index=True)
    aluno_id = Column(Integer, ForeignKey("alunos.id"), nullable=False)
    titulo = Column(String, nullable=False)
    descricao = Column(String, nullable=True)
    habilidade = Column(String, nullable=False)
    status = Column(String, default="pendente")
    data_criacao = Column(DateTime, default=datetime.utcnow)

    aluno = relationship("Aluno", back_populates="trilha")

# ===============================
# 📌 MODELO: Trilha de Estudo
# ===============================
class TrilhaDeEstudo(Base):
    __tablename__ = "trilhas_estudo"

    id = Column(Integer, primary_key=True, index=True)
    aluno_id = Column(Integer, ForeignKey("alunos.id"), nullable=False)
    leitura = Column(String, nullable=False)
    perguntas = Column(String, nullable=False)
    resumo_caligrafia = Column(String, nullable=True)
    link_video = Column(String, nullable=True)
    mini_prova = Column(String, nullable=True)
    meta_diaria = Column(String, nullable=True)
    meta_semanal = Column(String, nullable=True)
    data_criacao = Column(Date, default=date.today)

    aluno = relationship("Aluno", back_populates="trilhas_estudo")

# ===============================
# 📌 MODELO: Escrita Criativa
# ===============================
class EscritaCriativa(Base):
    __tablename__ = "escritas_criativas"

    id = Column(Integer, primary_key=True, index=True)
    aluno_id = Column(Integer, ForeignKey("alunos.id"), nullable=False)
    tema = Column(String, nullable=False)
    texto = Column(String, nullable=False)
    feedback = Column(String, nullable=True)
    data_envio = Column(Date, default=date.today)

    aluno = relationship("Aluno", back_populates="escritas")

# ===============================
# 📌 MODELO: Estudo Diário
# ===============================
class EstudoDiario(Base):
    __tablename__ = "estudos_diarios"

    id = Column(Integer, primary_key=True, index=True)
    aluno_id = Column(Integer, ForeignKey("alunos.id"), nullable=False)
    data = Column(Date, default=date.today, nullable=False)

    aluno = relationship("Aluno", back_populates="estudos_diarios")

# ===============================
# 📌 MODELO: Conquistas
# ===============================
class Conquista(Base):
    __tablename__ = "conquistas"

    id = Column(Integer, primary_key=True, index=True)
    aluno_id = Column(Integer, ForeignKey("alunos.id"), nullable=False)
    titulo = Column(String, nullable=False)
    descricao = Column(String, nullable=True)
    data_conquista = Column(Date, default=date.today)

    aluno = relationship("Aluno", back_populates="conquistas")

# ===============================
# 📌 MODELO: Resumo
# ===============================
class Resumo(Base):
    __tablename__ = "resumos"

    id = Column(Integer, primary_key=True, index=True)
    aluno_id = Column(Integer, ForeignKey("alunos.id"), nullable=False)
    conteudo = Column(Text, nullable=False)
    data = Column(DateTime, default=datetime.utcnow, nullable=False)

    aluno = relationship("Aluno", back_populates="resumos")

# ===============================
# 📌 MODELOS: Professores, Trabalhos e Entregas
# ===============================
class Professor(Base):
    __tablename__ = "professores"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    senha = Column(String, nullable=False)
    foto_url = Column(String, nullable=True)  # ✅ Adicione esta linha

    provas = relationship("ProvaPersonalizada", back_populates="professor")
    trabalhos = relationship("Trabalho", back_populates="professor")

class ProvaPersonalizada(Base):
    __tablename__ = "provas_personalizadas"

    id = Column(Integer, primary_key=True, index=True)
    professor_id = Column(Integer, ForeignKey("professores.id"), nullable=False)
    titulo = Column(String, nullable=False)
    descricao = Column(Text, nullable=True)
    data_criacao = Column(DateTime, default=datetime.utcnow)
    data_entrega = Column(Date, nullable=True)

    professor = relationship("Professor", back_populates="provas")

class Trabalho(Base):
    __tablename__ = "trabalhos"

    id = Column(Integer, primary_key=True, index=True)
    professor_id = Column(Integer, ForeignKey("professores.id"), nullable=False)
    titulo = Column(String, nullable=False)
    tema = Column(Text, nullable=True)
    prazo_entrega = Column(Date, nullable=True)
    criado_em = Column(DateTime, default=datetime.utcnow)

    professor = relationship("Professor", back_populates="trabalhos")

class RespostaAlunoTrabalho(Base):
    __tablename__ = "respostas_trabalho"

    id = Column(Integer, primary_key=True, index=True)
    trabalho_id = Column(Integer, ForeignKey("trabalhos.id"), nullable=False)
    aluno_id = Column(Integer, ForeignKey("alunos.id"), nullable=False)
    resposta = Column(Text, nullable=False)
    data_entrega = Column(DateTime, default=datetime.utcnow)

class EntregaTrabalho(Base):
    __tablename__ = "entregas_trabalho"

    id = Column(Integer, primary_key=True, index=True)
    trabalho_id = Column(Integer, ForeignKey("trabalhos.id"), nullable=False)
    aluno_id = Column(Integer, ForeignKey("alunos.id"), nullable=False)
    resposta = Column(Text, nullable=False)
    data_entrega = Column(DateTime, default=datetime.utcnow)

# ===============================
# 📌 MODELO: AlertaProva
# ===============================
class AlertaProva(Base):
    __tablename__ = "alertas_prova"

    id = Column(Integer, primary_key=True, index=True)
    data_alerta = Column(DateTime, nullable=False)
    mensagem = Column(String, nullable=False)
    tipo_alerta = Column(String, nullable=False)
    prova_id = Column(Integer, ForeignKey("provas.id"), nullable=False)

    prova = relationship("Prova", back_populates="alertas")

# ===============================
# 📌 MODELO: TarefaEstudo
# ===============================
class TarefaEstudo(Base):
    __tablename__ = "tarefas_estudo"

    id = Column(Integer, primary_key=True, index=True)
    aluno_id = Column(Integer, ForeignKey("alunos.id"), nullable=False)
    data = Column(Date, nullable=False)
    topicos = Column(String, nullable=False)
    status = Column(String, default="pendente")

    aluno = relationship("Aluno", back_populates="tarefas_estudo")

# ===============================
# 📌 MODELO: Agenda de Estudos
# ===============================
class AgendaEstudo(Base):
    __tablename__ = "agendas_estudo"

    id = Column(Integer, primary_key=True, index=True)
    aluno_id = Column(Integer, ForeignKey("alunos.id"), nullable=False)
    data_gerada = Column(Date, default=date.today)
    sugestao = Column(Text, nullable=False)

    aluno = relationship("Aluno")

class Materia(Base):
    __tablename__ = "materias"
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, unique=True, nullable=False)
    apostila_url = Column(String, nullable=True)

# 📚 MODELO: Apostila
class Apostila(Base):
    __tablename__ = "apostilas"

    id = Column(Integer, primary_key=True, index=True)
    materia = Column(String, nullable=False)
    capitulo = Column(String, nullable=False)
    titulo = Column(String, nullable=False)
    conteudo = Column(Text, nullable=False)












