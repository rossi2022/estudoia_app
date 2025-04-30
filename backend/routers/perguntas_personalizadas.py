from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.db import get_db
from backend.schemas import PerguntaOut
from backend.database.models import Aluno
from backend.ai_module import gerar_perguntas_por_materia

router = APIRouter()

@router.get("/personalizadas/{aluno_id}", response_model=list[PerguntaOut])
def perguntas_personalizadas(aluno_id: int, db: Session = Depends(get_db)):
    aluno = db.query(Aluno).filter(Aluno.id == aluno_id).first()
    if not aluno:
        raise HTTPException(status_code=404, detail="Aluno não encontrado")

    # 🔹 Simulação simples baseada em desempenho médio (nota mensal)
    nota_geral = sum(n.nota for n in aluno.notas) / len(aluno.notas) if aluno.notas else 5.0
    dificuldade = (
        "facil" if nota_geral < 5 else
        "media" if nota_geral < 8 else
        "dificil"
    )

    perguntas = gerar_perguntas_por_materia("Matemática", dificuldade)  # Exemplo com Matemática
    return [{"id": i+1, "materia": "Matemática", "pergunta": p, "resposta_correta": "", "dificuldade": dificuldade} for i, p in enumerate(perguntas)]

