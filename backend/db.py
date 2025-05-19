# File: backend/db.py

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# 1) URL do seu banco — ajuste se não for SQLite
SQLALCHEMY_DATABASE_URL = "sqlite:///./db.sqlite3"

# 2) Engine
#    - no SQLite é preciso desconectar a thread checagem
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False}
)

# 3) SessionLocal factory
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# 4) ÚNICO ponto de criação do Base
Base = declarative_base()

# 5) Dependência do FastAPI para injetar a sessão
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
