# File: backend/db.py

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os

# 🔹 Caminho do banco de dados (por padrão, SQLite local)
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./estudoia.db")

# 🔹 Criação do engine para conectar ao SQLite
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}  # necessário para SQLite em threads
)

# 🔹 Sessão de banco (ORM)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 🔹 Classe base para modelos declarativos
Base = declarative_base()

# 🔹 Criação das tabelas do banco
def create_db_tables():
    from backend.database import models  # ✅ importa os modelos para registrar
    Base.metadata.create_all(bind=engine)

# 🔹 Dependência do FastAPI para injetar a sessão do banco
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()







