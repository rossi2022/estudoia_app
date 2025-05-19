# ajustar_professores.py

import sqlite3

# Conecta ao banco SQLite
conn = sqlite3.connect("estudoia.db")  # ou o caminho correto do seu arquivo .db
cursor = conn.cursor()

# Adiciona a coluna foto_url se ainda não existir
try:
    cursor.execute("ALTER TABLE professores ADD COLUMN foto_url TEXT;")
    print("✅ Coluna 'foto_url' adicionada com sucesso na tabela 'professores'.")
except sqlite3.OperationalError as e:
    if "duplicate column name" in str(e):
        print("⚠️ A coluna 'foto_url' já existe.")
    else:
        print("❌ Erro:", e)

# Finaliza
conn.commit()
conn.close()
