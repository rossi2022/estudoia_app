from db import Base, engine
from database.models import Aluno, RespostaAluno, Prova, QuestaoProva, RespostaProva

# Cria todas as tabelas do banco de dados
Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)

print("✔️ Banco de dados resetado com sucesso!")











