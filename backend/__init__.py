# backend/init_db.py

from backend.db import Base, engine
from backend.database import models  # 👈 ESSENCIAL: isso registra os modelos

print("📦 Criando o banco de dados...")
Base.metadata.create_all(bind=engine)
print("✅ Banco de dados criado com sucesso.")
