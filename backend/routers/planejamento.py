from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import date, timedelta

from backend.db import get_db
from backend.database.models import Prova

router = APIRouter(
    prefix="/planejamento",
    tags=["Planejamento de Estudos"],
    responses={404: {"description": "Não encontrado"}}
)

@router.get("/{aluno_id}")
def get_planejamento(aluno_id: int, db: Session = Depends(get_db)):
    try:
        hoje = date.today()
        provas = (
            db.query(Prova)
              .filter(Prova.aluno_id == aluno_id, Prova.data_prova >= hoje)
              .order_by(Prova.data_prova)
              .all()
        )
        if not provas:
            raise HTTPException(status_code=404, detail="Nenhuma prova futura encontrada")

        planejamento = []
        for prova in provas:
            conteudos = [c.strip() for c in (prova.conteudo or "").split(",") if c.strip()]
            total = len(conteudos)
            dias = max((prova.data_prova.date() - hoje).days, 1)
            plano_dias = []
            for i in range(dias):
                data_i = hoje + timedelta(days=i)
                start = int(i * total / dias)
                end = int((i + 1) * total / dias)
                topicos = conteudos[start:end]
                plano_dias.append({
                    "data": data_i.isoformat(),
                    "topicos": topicos
                })
            planejamento.append({
                "prova_id": prova.id,
                "materia": prova.materia,
                "data_prova": prova.data_prova.date().isoformat(),
                "plano": plano_dias
            })

        return {"planejamento": planejamento}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



