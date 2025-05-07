import sys, os
sys.path.append(os.path.dirname(os.path.abspath(__file__ + '/../')))
import pandas as pd
from backend.db import SessionLocal
from backend.database.models import Apostila
from backend.database import models  # 👈 necessário para registrar os modelos

def popular_apostilas():
    print("📦 Lendo CSV...")
    df = pd.read_csv("backend/apostilas.csv", encoding="utf-8")
    session = SessionLocal()

    for _, row in df.iterrows():
        apostila = Apostila(
            materia=row["materia"],
            capitulo=row["capitulo"],
            titulo=row["titulo"],
            conteudo=row["conteudo"]
        )
        session.add(apostila)

    session.commit()
    session.close()
    print("✅ Apostilas inseridas com sucesso no banco!")

if __name__ == "__main__":
    print("📦 Criando o banco de dados...")
    popular_apostilas()
