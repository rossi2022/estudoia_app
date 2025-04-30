from db import SessionLocal
from database.models import Aluno, Pergunta

db = SessionLocal()

# Criar aluno
aluno = Aluno(nome="Teste Aluno", email="teste@teste.com", senha="1234", foto_url="foto.jpg")
db.add(aluno)
db.commit()
db.refresh(aluno)

# Adicionar perguntas de exemplo
perguntas = [
    Pergunta(materia="Matemática", pergunta_texto="Quanto é 2+2?", resposta_correta="4", dificuldade="easy"),
    Pergunta(materia="História", pergunta_texto="Quem descobriu o Brasil?", resposta_correta="Pedro Álvares Cabral", dificuldade="medium"),
]

for p in perguntas:
    db.add(p)

db.commit()
db.close()

print("Banco de dados populado com dados de exemplo.")
