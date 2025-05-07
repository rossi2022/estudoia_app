# File: backend/criar_materias_db.py

from db import Base, engine, SessionLocal
from database.models import Materia

# 📌 Criação do banco
print("📦 Criando o banco de dados com matérias...")
Base.metadata.create_all(bind=engine)

# 📌 Lista de matérias fixas
materias_fixas = [
    "Matemática",
    "Português",
    "História",
    "Geografia",
    "Física",
    "Química",
    "Biologia",
    "Inglês",
    "Literatura",
    "Artes",
    "Gramática",
    "Sociologia",
    "Filosofia",
    "Redação"
]

# 📌 Inserção no banco
db = SessionLocal()
for nome in materias_fixas:
    if not db.query(Materia).filter_by(nome=nome).first():
        materia = Materia(nome=nome, apostila_url=None)
        db.add(materia)

db.commit()
db.close()

print("✅ Banco de dados populado com as matérias.")
