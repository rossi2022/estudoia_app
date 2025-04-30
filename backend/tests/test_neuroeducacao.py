# backend/routers/neuroeducacao.py
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import Response
from sqlalchemy.orm import Session
from backend.db import get_db
from fpdf import FPDF
from io import BytesIO
from backend.database.models import Aluno

router = APIRouter()

@router.get("/neuroeducacao/{aluno_id}")
def gerar_pdf_neuroeducacao(aluno_id: int, db: Session = Depends(get_db)):
    aluno = db.query(Aluno).filter(Aluno.id == aluno_id).first()
    if not aluno:
        raise HTTPException(status_code=404, detail="Aluno não encontrado")

    # Exemplo de conteúdo para o PDF
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="Atividades de Neuroeducação", ln=1, align="C")
    pdf.cell(200, 10, txt=f"Aluno: {aluno.nome}", ln=2)

    output = BytesIO()
    pdf.output(output)
    output.seek(0)

    return Response(content=output.read(), media_type="application/pdf")



