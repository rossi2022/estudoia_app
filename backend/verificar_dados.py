# verificar_dados.py

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from backend.database.models import Aluno, NotaMensal
from backend.db import Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "sqlite:///./estudoia.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine)
db = SessionLocal()

print("🔎 Alunos cadastrados:")
alunos = db.query(Aluno).order_by(Aluno.id.desc()).all()
for aluno in alunos:
    print(f"ID: {aluno.id}, Nome: {aluno.nome}, Email: {aluno.email}")

print("\n🧠 Notas Mensais cadastradas:")
notas = db.query(NotaMensal).order_by(NotaMensal.id.desc()).all()
for nota in notas:
    print(f"Aluno ID: {nota.aluno_id}, Matéria: {nota.materia}, Nota: {nota.nota}, Mês: {nota.mes}")

   
