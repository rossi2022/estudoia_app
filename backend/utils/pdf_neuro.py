# utils/pdf_neuro.py
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from io import BytesIO

def gerar_pdf_neuroeducacao(aluno_nome: str) -> bytes:
    buffer = BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=A4)
    largura, altura = A4

    pdf.setTitle("Atividades de Neuroeducação")

    # Cabeçalho
    pdf.setFont("Helvetica-Bold", 18)
    pdf.drawCentredString(largura / 2, altura - 50, "Atividades de Neuroeducação")
    pdf.setFont("Helvetica", 12)
    pdf.drawString(50, altura - 80, f"Aluno: {aluno_nome}")

    # Exercício 1 - Sequência lógica
    pdf.setFont("Helvetica-Bold", 14)
    pdf.drawString(50, altura - 120, "1. Sequência Lógica")
    pdf.setFont("Helvetica", 12)
    pdf.drawString(70, altura - 140, "Complete: 2, 4, 6, ___, ___, ___")

    # Exercício 2 - Jogo da memória
    pdf.setFont("Helvetica-Bold", 14)
    pdf.drawString(50, altura - 180, "2. Jogo da Memória")
    pdf.setFont("Helvetica", 12)
    pdf.drawString(70, altura - 200, "Observe as figuras (imaginárias) e tente memorizá-las por 30 segundos.")
    pdf.drawString(70, altura - 215, "(Exemplo: 🍎🐶🚗🎈🧩) Depois, escreva o que você lembra.")

    # Exercício 3 - Labirinto visual
    pdf.setFont("Helvetica-Bold", 14)
    pdf.drawString(50, altura - 250, "3. Labirinto Visual (Visualize ou desenhe)")
    pdf.setFont("Helvetica", 12)
    pdf.drawString(70, altura - 270, "Desenhe um labirinto simples no papel e tente sair dele com lápis.")

    # Rodapé
    pdf.setFont("Helvetica-Oblique", 10)
    pdf.drawString(50, 40, "Essas atividades ajudam a desenvolver atenção, memória e raciocínio lógico.")

    pdf.showPage()
    pdf.save()
    buffer.seek(0)
    return buffer.getvalue()

