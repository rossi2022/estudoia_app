# backend/routers/responder_prova.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.db import get_db
from backend.database.models import ProvaPersonalizada, Trabalho

router = APIRouter(
    prefix="/estudos",
    tags=["Responder Provas"]
)

# 📚 Enviar Respostas de uma Prova
@router.post("/provas/{prova_id}/responder")
def responder_prova(prova_id: int, respostas: dict, db: Session = Depends(get_db)):
    prova = db.query(ProvaPersonalizada).filter(ProvaPersonalizada.id == prova_id).first()

    if not prova:
        raise HTTPException(status_code=404, detail="Prova não encontrada.")

    # 📌 OBS: Aqui seria a lógica para comparar as respostas (não implementado ainda porque depende de como você quer armazenar as questões)
    # Por enquanto, vamos só simular:
    total_questoes = len(respostas)
    acertos_simulados = int(total_questoes * 0.8)  # 📌 Simulando 80% de acertos para teste

    nota_final = (acertos_simulados / total_questoes) * 10

    return {
        "mensagem": "Prova respondida!",
        "prova_id": prova_id,
        "total_questoes": total_questoes,
        "acertos": acertos_simulados,
        "nota_final": round(nota_final, 2)
    }
