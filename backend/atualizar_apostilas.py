# File: backend/atualizar_apostilas.py

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from backend.db import SessionLocal
from backend.database.models import Materia

# 🔗 Dicionário com os caminhos dos PDFs
PDFS = {
    "Matemática": "/static/apostilas/matematica.pdf",
    "Português": "/static/apostilas/portugues.pdf",
    "História": "/static/apostilas/historia.pdf",
    "Geografia": "/static/apostilas/geografia.pdf",
    "Física": "/static/apostilas/fisica.pdf",
    "Química": "/static/apostilas/quimica.pdf",
    "Biologia": "/static/apostilas/biologia.pdf",
    "Inglês": "/static/apostilas/ingles.pdf",
    "Literatura": "/static/apostilas/literatura.pdf",
    "Artes": "/static/apostilas/artes.pdf",
    "Gramática": "/static/apostilas/gramatica.pdf",
    "Sociologia": "/static/apostilas/sociologia.pdf",
    "Filosofia": "/static/apostilas/filosofia.pdf",
    "Redação": "/static/apostilas/redacao.pdf"
}

def atualizar_apostilas():
    db = SessionLocal()
    for nome, url in PDFS.items():
        materia = db.query(Materia).filter_by(nome=nome).first()
        if materia:
            materia.apostila_url = url
    db.commit()
    db.close()
    print("✅ URLs das apostilas atualizadas com sucesso!")

if __name__ == "__main__":
    atualizar_apostilas()
