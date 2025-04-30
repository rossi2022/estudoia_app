from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.db import get_db
from backend.database.models import HistoricoDesempenho, Aluno
from datetime import date
from backend.schemas import PerguntaOut, EstudoDiarioIn
from backend.openai_api import gerar_perguntas_por_materia

router = APIRouter()

# ✅ Rota 1: Registrar o dia de estudo (com contagem)
@router.post("/registrar")
def registrar_estudo_diario(payload: EstudoDiarioIn, db: Session = Depends(get_db)):
    aluno_id = payload.aluno_id

    aluno = db.query(Aluno).filter(Aluno.id == aluno_id).first()
    if not aluno:
        raise HTTPException(status_code=404, detail="Aluno não encontrado")

    registro = HistoricoDesempenho(
        aluno_id=aluno_id,
        materia="geral",
        acertos=0,
        erros=0,
        data=date.today()
    )
    db.add(registro)
    db.commit()

    total_dias = db.query(HistoricoDesempenho).filter(HistoricoDesempenho.aluno_id == aluno_id).count()

    return {
        "mensagem": "Estudo diário registrado com sucesso",
        "total_dias": total_dias
    }

# ✅ Rota 2: Obter perguntas com base nos erros do histórico
@router.get("/diario/{aluno_id}", response_model=list[PerguntaOut])
def estudo_diario(aluno_id: int, db: Session = Depends(get_db)):
    aluno = db.query(Aluno).filter(Aluno.id == aluno_id).first()
    if not aluno:
        raise HTTPException(status_code=404, detail="Aluno não encontrado")

    desempenho = db.query(HistoricoDesempenho).filter(HistoricoDesempenho.aluno_id == aluno_id).all()
    if not desempenho:
        return []

    desempenho.sort(key=lambda x: x.erros, reverse=True)
    materias_dificeis = [d.materia for d in desempenho[:3]]

    perguntas = []
    for materia in materias_dificeis:
        geradas = gerar_perguntas_por_materia(materia, dificuldade="media")
        perguntas.extend([
            {"id": 0, "materia": materia, "pergunta": p, "resposta_correta": "", "dificuldade": "media"}
            for p in geradas
        ])

    return perguntas[:10]




