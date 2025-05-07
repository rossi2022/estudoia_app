# File: backend/routers/relatorio_pdf.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.db import get_db
from backend.database.models import Aluno, NotaMensal
from fastapi.responses import FileResponse
import os
from fpdf import FPDF
from datetime import date

router = APIRouter(
    prefix="/relatorio-pdf",
    tags=["relatorio"]
)

@router.get("/{aluno_id}", response_class=FileResponse)
def gerar_relatorio_pdf(aluno_id: int, db: Session = Depends(get_db)):
    aluno = db.query(Aluno).filter(Aluno.id == aluno_id).first()
    if not aluno:
        raise HTTPException(status_code=404, detail="Aluno não encontrado")

    notas = db.query(NotaMensal).filter(NotaMensal.aluno_id == aluno_id).all()
    media_geral = sum(n.nota for n in notas) / len(notas) if notas else 0.0

    if media_geral >= 9.0:
        mensagem = "Excelente trabalho! Continue assim!"
    elif media_geral >= 7.0:
        mensagem = "Muito bem! Você está indo no caminho certo!"
    elif media_geral >= 5.0:
        mensagem = "Você consegue melhorar, mantenha o foco!"
    else:
        mensagem = "Vamos reforçar o aprendizado!"

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt=f"Relatório Mensal - {aluno.nome}", ln=True, align="C")
    pdf.ln(10)
    pdf.cell(200, 10, txt=f"E-mail: {aluno.email}", ln=True)
    pdf.cell(200, 10, txt=f"Data: {date.today().strftime('%d/%m/%Y')}", ln=True)
    pdf.ln(5)
    for nota in notas:
        pdf.cell(200, 10, txt=f"{nota.materia}: {nota.nota} ({nota.mes})", ln=True)
    pdf.ln(5)
    pdf.cell(200, 10, txt=f"Média Geral: {round(media_geral, 2)}", ln=True)
    pdf.multi_cell(0, 10, txt=f"Mensagem: {mensagem}")

    filepath = f"relatorio_{aluno_id}.pdf"
    pdf.output(filepath)
    return FileResponse(path=filepath, filename=filepath, media_type='application/pdf')
