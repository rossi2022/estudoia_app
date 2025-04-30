# backend/routers/neuroeducacao.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.responses import FileResponse
from backend.db import get_db
from backend.database.models import Aluno
from datetime import datetime
from fpdf import FPDF
import os

router = APIRouter()

@router.get("/{aluno_id}")
def gerar_pdf_neuroeducacao(aluno_id: int, db: Session = Depends(get_db)):
    aluno = db.query(Aluno).filter(Aluno.id == aluno_id).first()
    if not aluno:
        raise HTTPException(status_code=404, detail="Aluno não encontrado")

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=14)

    pdf.cell(200, 10, txt="Atividades de Neuroeducação", ln=True, align="C")
    pdf.ln(10)
    pdf.set_font("Arial", size=12)

    pdf.cell(200, 10, txt=f"Nome do Aluno: {aluno.nome}", ln=True)
    pdf.cell(200, 10, txt=f"Data: {datetime.now().strftime('%d/%m/%Y')}", ln=True)
    pdf.ln(10)

    atividades = [
        "🔷 Complete a sequência: 2, 4, 6, __, __",
        "🔷 Lembre-se das 5 palavras a seguir: Casa, Flor, Cadeira, Peixe, Sol. Agora, escreva-as sem olhar.",
        "🔷 Encontre o caminho no labirinto (desenhar em anexo)",
        "🔷 Qual é a próxima figura da sequência? ◼️ 🔺 ◻️ 🔺 ◼️ 🔺 __",
        "🔷 Faça uma respiração profunda por 1 minuto e escreva como se sentiu.",
    ]

    for atividade in atividades:
        pdf.multi_cell(0, 10, txt=atividade)
        pdf.ln(3)

    pasta = "atividades_neuro"
    if not os.path.exists(pasta):
        os.makedirs(pasta)

    caminho_pdf = os.path.join(pasta, f"neuroeducacao_{aluno.id}.pdf")
    pdf.output(caminho_pdf)

    return FileResponse(path=caminho_pdf, filename=f"neuroeducacao_{aluno.nome}.pdf", media_type='application/pdf')



