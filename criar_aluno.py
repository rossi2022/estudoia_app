# File: criar_aluno.py

from backend.db import SessionLocal
from backend.database.models import Aluno
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
db = SessionLocal()

# Verifica se já existe
email = "joao@example.com"
aluno_existente = db.query(Aluno).filter_by(email=email).first()

if aluno_existente:
    print("❗ Aluno já existe.")
else:
    senha_criptografada = pwd_context.hash("1234")
    novo_aluno = Aluno(
        nome="João da Silva",
        email=email,
        senha=senha_criptografada
    )
    db.add(novo_aluno)
    db.commit()
    print("✅ Aluno criado com sucesso.")
