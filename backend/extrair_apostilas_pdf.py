import fitz  # PyMuPDF
import os
import pandas as pd

# Caminho da pasta onde estão os PDFs
pasta_apostilas = "frontend/static/apostilas"
linhas_csv = []

for materia in os.listdir(pasta_apostilas):
    caminho_materia = os.path.join(pasta_apostilas, materia)
    if not os.path.isdir(caminho_materia):
        continue

    for arquivo in os.listdir(caminho_materia):
        if arquivo.endswith(".pdf"):
            capitulo = os.path.splitext(arquivo)[0]
            caminho_pdf = os.path.join(caminho_materia, arquivo)

            try:
                with fitz.open(caminho_pdf) as doc:
                    conteudo = ""
                    for pagina in doc:
                        conteudo += pagina.get_text()

                    linhas_csv.append({
                        "materia": materia,
                        "capitulo": capitulo,
                        "titulo": f"{materia} - {capitulo}",
                        "conteudo": conteudo.strip().replace('\n', ' ')
                    })
            except Exception as e:
                print(f"Erro ao processar {caminho_pdf}: {e}")

# Gera CSV com todos os dados extraídos
df = pd.DataFrame(linhas_csv)
csv_path = "backend/apostilas.csv"
df.to_csv(csv_path, index=False, encoding="utf-8")
print(f"✅ CSV gerado com sucesso em {csv_path}")


