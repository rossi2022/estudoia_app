from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import FileResponse
from backend.db import get_db
from sqlalchemy.orm import Session
from backend.database.models import Aluno
import os
from fpdf import FPDF
from datetime import date
from pathlib import Path

# 🔹 Prefixo corrigido para funcionar com prefix="/api" no main.py
router = APIRouter(
    prefix="/caligrafia",
    tags=["Caligrafia"]
)

@router.get("/{aluno_id}", response_description="Gera PDF de exercícios de caligrafia personalizado")
async def gerar_pdf_caligrafia(aluno_id: int, db: Session = Depends(get_db)):
    # Verifica se o aluno existe
    aluno = db.query(Aluno).filter(Aluno.id == aluno_id).first()
    if not aluno:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Aluno não encontrado"
        )

    try:
        # Cria diretório se não existir
        output_dir = Path("backend/arquivos")
        output_dir.mkdir(exist_ok=True, parents=True)

        # Sanitiza o nome: só alfanuméricos, sublinhado e hífen, e converte espaços em _
        raw = "".join(c if c.isalnum() or c in "_-" else " " for c in aluno.nome)
        nome_sanitizado = "_".join(raw.split())

        # Monta nome e caminho do arquivo
        nome_arquivo = f"caligrafia_{nome_sanitizado}_{date.today()}.pdf"
        caminho_arquivo = output_dir / nome_arquivo

        # Cria o PDF
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=16)
        pdf.cell(200, 10, txt=f"Exercícios de Caligrafia - {aluno.nome}", ln=True, align="C")
        pdf.set_font("Arial", size=12)
        pdf.ln(10)

        # Seção de letras
        pdf.cell(200, 10, txt="Pratique as letras:", ln=True)
        letras = ["A", "B", "C", "D", "E", "F", "G", "H"]
        for letra in letras:
            pdf.cell(200, 10,
                     txt=f"{letra} {letra} {letra} {letra}    {letra.lower()} {letra.lower()} {letra.lower()} {letra.lower()}",
                     ln=True)
        pdf.ln(5)

        # Seção de palavras
        pdf.cell(200, 10, txt="Pratique as palavras:", ln=True)
        palavras = ["Amor", "Beleza", "Cuidado", "Dedicação", "Educação", "Família"]
        for palavra in palavras:
            pdf.cell(200, 10, txt=f"{palavra}, {palavra}, {palavra}", ln=True)
        pdf.ln(5)

        # Seção do nome do aluno
        pdf.cell(200, 10, txt="Escreva seu nome 3 vezes:", ln=True)
        for _ in range(3):
            pdf.cell(200, 10, txt="_____________________________", ln=True)
        pdf.ln(5)

        # Seção de frase
        pdf.cell(200, 10, txt="Escreva a frase abaixo:", ln=True)
        pdf.cell(200, 10, txt="A prática leva à perfeição!", ln=True)
        for _ in range(3):
            pdf.cell(200, 10, txt="_____________________________", ln=True)

        # Gera o PDF no disco
        pdf.output(caminho_arquivo)

        # Verifica se o arquivo foi criado
        if not caminho_arquivo.exists():
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Falha ao gerar o PDF"
            )

        return FileResponse(
            caminho_arquivo,
            media_type="application/pdf",
            filename=nome_arquivo
        )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao gerar PDF: {str(e)}"
        )




