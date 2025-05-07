import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from db import SessionLocal, engine, Base
from database.models import Materia

Base.metadata.create_all(bind=engine)

# 📁 Caminho da pasta onde estão os PDFs
PASTA_APOSTILAS = os.path.join("frontend", "static", "apostilas")

# 🧠 Lista de matérias com os nomes dos arquivos PDF correspondentes
materias_com_pdf = {
    "Arte": "Arte_Capitulo_04_Geekie.pdf",
    "Matemática": "matematica_basica.pdf",
    "História": "historia_resumo.pdf",
    # Adicione mais se quiser
}

def inserir_ou_atualizar_materias():
    db = SessionLocal()
    for nome, arquivo in materias_com_pdf.items():
        caminho_pdf = f"/static/apostilas/{arquivo}"
        materia_existente = db.query(Materia).filter_by(nome=nome).first()

        if materia_existente:
            if not materia_existente.apostila_url:
                materia_existente.apostila_url = caminho_pdf
                print(f"🔁 Atualizando apostila da matéria '{nome}'.")
            else:
                print(f"⚠️ Matéria '{nome}' já possui PDF. Pulando...")
        else:
            nova_materia = Materia(nome=nome, apostila_url=caminho_pdf)
            db.add(nova_materia)
            print(f"✅ Inserindo nova matéria: {nome}")
    db.commit()
    db.close()
    print("🎓 Inserção/atualização concluída.")

if __name__ == "__main__":
    inserir_ou_atualizar_materias()

