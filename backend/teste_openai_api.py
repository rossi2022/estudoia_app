import os
import sys
from dotenv import load_dotenv

# Adiciona o diretório raiz ao sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from backend.openai_api import gerar_perguntas_personalizadas
from backend.db import SessionLocal
from backend.database.models import Aluno

# Carrega variáveis do .env
load_dotenv()

# Solicita ID do aluno
try:
    aluno_id = int(input("Digite o ID do aluno para gerar perguntas personalizadas: "))
except ValueError:
    print("❌ ID inválido. Digite um número inteiro.")
    exit()

# Inicializa sessão do banco
db = SessionLocal()

# Busca o aluno
aluno = db.query(Aluno).filter(Aluno.id == aluno_id).first()
if aluno:
    print(f"\n🔍 Gerando perguntas personalizadas para: {aluno.nome}")
else:
    print("❌ Aluno não encontrado.")
    db.close()
    exit()

# Gera perguntas com base no desempenho
perguntas = gerar_perguntas_personalizadas(aluno_id, db)

# Exibe as perguntas geradas
print("\n📚 Perguntas Personalizadas:")
if perguntas:
    for i, pergunta in enumerate(perguntas, 1):
        print(f"{i}. {pergunta}")
else:
    print("⚠️ Nenhuma pergunta foi gerada.")

db.close()

