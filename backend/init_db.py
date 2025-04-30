# backend/init_db.py

import sys
import os

# Adiciona o caminho correto para conseguir importar backend.*
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from backend.db import Base, engine
from backend.database import models

print("Criando todas as tabelas...")
Base.metadata.create_all(bind=engine)
print("✅ Tabelas criadas com sucesso.")






