from backend.db import SessionLocal
from backend.database.models import Pergunta
from backend.perguntas_fixas import perguntas_fixas

def popular_perguntas():
    db = SessionLocal()
    for p in perguntas_fixas:
        pergunta_existente = db.query(Pergunta).filter_by(
            materia=p["materia"],
            enunciado=p["enunciado"]
        ).first()

        if not pergunta_existente:
            nova_pergunta = Pergunta(
                materia=p["materia"],
                enunciado=p["enunciado"],
                resposta_correta=p["resposta_correta"],
                dificuldade=p["dificuldade"]
            )
            db.add(nova_pergunta)

    db.commit()
    db.close()
    print("✅ Perguntas fixas inseridas com sucesso!")

if __name__ == "__main__":
    popular_perguntas()
