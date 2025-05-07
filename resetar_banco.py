import os

# Caminho do arquivo SQLite
db_path = "estudoia.db"

# Remove o banco de dados existente
if os.path.exists(db_path):
    os.remove(db_path)
    print("🗑️ Banco de dados antigo removido.")
else:
    print("ℹ️ Nenhum banco anterior encontrado.")

# Recria as tabelas
from backend.db import create_db_tables
create_db_tables()
print("✅ Novo banco de dados criado com sucesso.")

# Popula com dados de exemplo
import backend.popular_banco
