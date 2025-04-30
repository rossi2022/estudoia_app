from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database.models import Base


DATABASE_URL = "sqlite:///./estudoia.db"  # Caminho para o banco de dados SQLite
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

# Criação das tabelas no banco de dados
Base.metadata.create_all(bind=engine)
print("Tabelas criadas com sucesso.")










