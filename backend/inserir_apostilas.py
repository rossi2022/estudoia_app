# File: backend/popular_apostilas.py
import pandas as pd
from sqlalchemy.orm import Session
from backend.db import SessionLocal  # ✅ Corrigido
from backend.database.models import Apostila

def popular_apostilas():
    session: Session = SessionLocal()

    df = pd.read_csv("backend/apostilas.csv", encoding="utf-8")

    for _, row in df.iterrows():
        apostila = Apostila(
            materia=row['materia'],
            capitulo=row['capitulo'],
            titulo=row['titulo'],
            conteudo=row['conteudo']
        )
        session.add(apostila)

    session.commit()
    session.close()
    print("✅ Apostilas inseridas com sucesso no banco!")

if __name__ == "__main__":
    popular_apostilas()
