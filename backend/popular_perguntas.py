# backend/popular_perguntas.py

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from backend.db import SessionLocal
from backend.database.models import Pergunta
from backend.perguntas_fixas import perguntas_fixas

def popular_perguntas():
    db = SessionLocal()
    for p in perguntas_fixas:
        existe = db.query(Pergunta).filter_by(
            materia=p["materia"],
            enunciado=p["enunciado"]
        ).first()
        if not existe:
            nova = Pergunta(
                materia=p["materia"],
                enunciado=p["enunciado"],
                resposta_correta=p["resposta_correta"],
                dificuldade=p["dificuldade"]
            )
            db.add(nova)
    db.commit()
    db.close()
    print("✅ Perguntas fixas inseridas com sucesso!")

if __name__ == "__main__":
    popular_perguntas()
