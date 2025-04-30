# adicionar_nota.py

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from backend.db import Base
from backend.database.models import NotaMensal
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "sqlite:///./estudoia.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine)
db = SessionLocal()

# 🔹 Altere aqui o ID do aluno e os dados da nota
aluno_id = 1
materia = "Matemática"
nota = 9.5
mes = "Abril"

nova_nota = NotaMensal(
    aluno_id=aluno_id,
    materia=materia,
    nota=nota,
    mes=mes
)

db.add(nova_nota)
db.commit()

print(f"✅ Nota adicionada: Aluno {aluno_id} - {materia} - {nota} ({mes})")
