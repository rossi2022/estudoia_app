# deletar_aluno.py

import sqlite3

# Caminho para o banco
db_path = "estudoia.db"

# Altere o ID do aluno a ser deletado
aluno_id = 1

# Conecta no banco
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Deleta o aluno
cursor.execute("DELETE FROM alunos WHERE id = ?", (aluno_id,))
conn.commit()

# Confirma se foi excluído
if cursor.rowcount > 0:
    print(f"✅ Aluno com ID {aluno_id} deletado com sucesso.")
else:
    print(f"⚠️ Nenhum aluno com ID {aluno_id} encontrado.")

conn.close()
