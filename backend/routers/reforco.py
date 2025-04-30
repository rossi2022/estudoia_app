# backend/routers/reforco.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.db import get_db
from backend.database.models import RespostaAluno

router = APIRouter(
    prefix="/reforco",
    tags=["Reforço"]
)

@router.get("/{aluno_id}")
def gerar_reforco_personalizado(aluno_id: int, db: Session = Depends(get_db)):
    respostas = db.query(RespostaAluno).filter(RespostaAluno.aluno_id == aluno_id).all()

    if not respostas:
        raise HTTPException(status_code=404, detail="Nenhuma resposta encontrada para este aluno.")

    desempenho = {}
    for resposta in respostas:
        materia = resposta.materia
        acertou = resposta.correta.lower() == "true"  # 🔥 Mudança aqui

        if materia not in desempenho:
            desempenho[materia] = {"total": 0, "quantidade": 0}

        desempenho[materia]["total"] += 1 if acertou else 0
        desempenho[materia]["quantidade"] += 1

    reforcos = []
    for materia, dados in desempenho.items():
        media = dados["total"] / dados["quantidade"]
        if media < 0.6:  # 🔹 Média de acertos menor que 60% pede reforço
            reforcos.append({
                "materia": materia,
                "media": round(media * 10, 2),  # Opcional: converter para nota de 0 a 10
                "sugestao": f"Reforçar conteúdos de {materia}. Média atual: {round(media * 10, 2)}"
            })

    return {"reforcos_sugeridos": reforcos}







