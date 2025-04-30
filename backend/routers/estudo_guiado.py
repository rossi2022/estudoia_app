# File: backend/routers/estudo_guiado.py

from fastapi import APIRouter, Query

router = APIRouter(
    prefix="/guiado",
    tags=["Estudo Guiado"]
)

@router.get("/pergunta")
def guia_pergunta(
    materia: str = Query(..., description="Disciplina, ex: História"),
    topico: str = Query(..., description="Tópico ou enunciado da pergunta")
):
    """
    Retorna instruções de estudo guiado para o aluno antes de entregar a resposta.
    """
    instrucoes = (
        f"📒 Para responder sobre '{topico}' em {materia}, pegue um caderno e lápis. "
        f"📖 Consulte as páginas correspondentes da apostila de {materia} (por exemplo, capítulos ou seções relevantes) "
        "e faça anotações dos pontos principais. ✍️ Só depois elabore sua resposta baseada nessas anotações."
    )
    return {"instrucoes": instrucoes}
