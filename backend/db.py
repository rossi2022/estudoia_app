# File: backend/db.py

import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# 🔧 Base para declaração de modelos
Base = declarative_base()

# 🔧 Configuração do banco de dados (via DATABASE_URL ou SQLite local)
SQLALCHEMY_DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "sqlite:///./estudoia.db"
)

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False}
    if SQLALCHEMY_DATABASE_URL.startswith("sqlite")
    else {}
)

# 🔧 Sessão para injeção nas rotas
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# 🔧 Importa todos os seus modelos para o metadata
import backend.database.models  # noqa: F401

# 🔧 Cria todas as tabelas assim que este módulo for importado
Base.metadata.create_all(bind=engine)

def get_db():
    """
    Dependência do FastAPI para fornecer uma sessão de DB
    e fechá-la ao final da requisição.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



