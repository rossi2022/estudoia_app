from backend.db import SessionLocal, create_db_tables
from backend.database import models
from passlib.context import CryptContext
from datetime import datetime, date

# 🔐 Criptografia de senha
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# 🔹 Cria tabelas (se ainda não estiverem criadas)
create_db_tables()

# 🔹 Sessão de banco
db = SessionLocal()

print("📦 Criando o banco de dados...")

# 🔹 Criação do aluno com senha hasheada
aluno = models.Aluno(
    nome="João da Silva",
    email="joao@example.com",
    senha=pwd_context.hash("1234")  # ✅ Agora a senha está criptografada
)
db.add(aluno)
db.commit()
db.refresh(aluno)

# 🔹 Prova e questão de exemplo
prova = models.Prova(
    aluno_id=aluno.id,
    nome="Prova de Matemática",
    data_prova=datetime.now(),
    nota_final=0.0,
    conteudo="Conteúdo de matemática básica"
)
db.add(prova)
db.commit()
db.refresh(prova)

# 🔹 Pergunta associada
pergunta = models.Pergunta(
    materia="Matemática",
    enunciado="Quanto é 2 + 2?",
    resposta_correta="4",
    dificuldade="fácil"
)
db.add(pergunta)
db.commit()
db.refresh(pergunta)

# 🔹 Questão associada à prova
questao = models.QuestaoProva(
    prova_id=prova.id,
    pergunta_id=pergunta.id
)
db.add(questao)
db.commit()

# 🔹 Recompensa
recompensa = models.Recompensa(
    aluno_id=aluno.id,
    tipo="Boas-vindas",
    descricao="Primeira conquista por acessar o sistema!",
    data=str(date.today())
)
db.add(recompensa)

# 🔹 Trilha de aprendizado
trilha = models.TrilhaAprendizado(
    aluno_id=aluno.id,
    titulo="Revolução Francesa",
    descricao="Entender as causas e consequências",
    habilidade="Interpretação Histórica"
)
db.add(trilha)

# 🔹 Estudo diário
estudo = models.EstudoDiario(
    aluno_id=aluno.id
)
db.add(estudo)

# 🔹 Escrita Criativa
escrita = models.EscritaCriativa(
    aluno_id=aluno.id,
    tema="O que aprendi hoje",
    texto="Hoje aprendi sobre frações.",
    feedback="Excelente!"
)
db.add(escrita)

# 🔹 Histórico
historico = models.HistoricoDesempenho(
    aluno_id=aluno.id,
    materia="Matemática",
    acertos=3,
    erros=1
)
db.add(historico)

# 🔹 Resumo
resumo = models.Resumo(
    aluno_id=aluno.id,
    conteudo="Resumo sobre células e fotossíntese."
)
db.add(resumo)

# 🔹 Finaliza
db.commit()
db.close()

print("✅ Banco populado com dados de teste.")





