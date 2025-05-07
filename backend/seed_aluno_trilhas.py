# File: backend/seed_aluno_trilhas.py

import sys
import os

# 🔧 Adiciona o diretório raiz ao sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.db import SessionLocal
from backend.database.models import Aluno, TrilhaAprendizado
from datetime import datetime

db = SessionLocal()

# 🔹 Aluno de teste
aluno_teste = {
    "id": 9,
    "nome": "Aluno de Teste",
    "email": "teste9@estudoia.com",
    "senha": "123",
    "foto_url": "/static/img/default-avatar.png"
}

# 🔹 Metas para inserir
metas = [
    {
        "aluno_id": 9,
        "titulo": "Ler 2 páginas por dia",
        "descricao": "Praticar leitura leve diariamente",
        "habilidade": "Leitura fluente",
        "status": "pendente",
        "data_criacao": datetime.utcnow()
    },
    {
        "aluno_id": 9,
        "titulo": "Revisar Matemática básica",
        "descricao": "Focar em frações e porcentagem",
        "habilidade": "Raciocínio lógico",
        "status": "pendente",
        "data_criacao": datetime.utcnow()
    }
]

def popular_aluno_e_trilhas():
    try:
        aluno = db.query(Aluno).filter_by(id=aluno_teste["id"]).first()
        if not aluno:
            aluno = Aluno(**aluno_teste)
            db.add(aluno)
            db.commit()
            print(f"✅ Aluno {aluno.nome} criado com sucesso.")
        else:
            print(f"⚠️ Aluno com id {aluno.id} já existe.")

        for meta in metas:
            existe_meta = db.query(TrilhaAprendizado).filter_by(
                aluno_id=meta["aluno_id"],
                titulo=meta["titulo"]
            ).first()
            if not existe_meta:
                nova_trilha = TrilhaAprendizado(**meta)
                db.add(nova_trilha)
        db.commit()
        print("✅ Metas inseridas com sucesso.")
    except Exception as e:
        print("❌ Erro ao popular dados:", e)
    finally:
        db.close()

if __name__ == "__main__":
    popular_aluno_e_trilhas()
