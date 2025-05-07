# File: backend/popular_professor.py

from backend.db import SessionLocal
from backend.database.models import Professor
from backend.utils.security import get_password_hash

# ✅ Cria a sessão com o banco
session = SessionLocal()

# 🔐 Dados do professor
nome = "Professor João"
email = "joao@example.com"
senha = "senha123"
senha_hash = get_password_hash(senha)

# 🔍 Verifica se já existe
professor_existente = session.query(Professor).filter(Professor.email == email).first()
if professor_existente:
    print("⚠️ Professor já cadastrado.")
else:
    novo_professor = Professor(nome=nome, email=email, senha=senha_hash)
    session.add(novo_professor)
    session.commit()
    print("✅ Professor cadastrado com sucesso!")

# 🔒 Fecha a sessão
session.close()
