from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from backend.db import get_db
from backend.database.models import Aluno, Medalha
from backend.schemas import MedalhaOut, MedalhasDoAluno

router = APIRouter(
    prefix="/medalhas",
    tags=["medalhas"]
)

@router.get(
    "/{aluno_id}",
    response_model=MedalhasDoAluno,
    status_code=status.HTTP_200_OK
)
def get_medalhas_do_aluno(aluno_id: int, db: Session = Depends(get_db)):
    """
    Retorna todas as medalhas conquistadas por um aluno, junto com o nome do aluno.
    """
    try:
        aluno = db.query(Aluno).filter(Aluno.id == aluno_id).first()
        if not aluno:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Aluno não encontrado."
            )

        medalhas = db.query(Medalha).filter(Medalha.aluno_id == aluno_id).all()

        # Mapeia cada objeto SQLAlchemy para o schema Pydantic
        medalhas_out: List[MedalhaOut] = []
        for m in medalhas:
            medalhas_out.append(
                MedalhaOut(
                    id=m.id,
                    titulo=m.titulo,
                    descricao=m.descricao,
                    # Ajusta para usar o campo correto do model:
                    data_conquista=getattr(m, "data_conquista", None) or getattr(m, "data", None)
                )
            )

        return MedalhasDoAluno(
            aluno_id=aluno.id,
            nome=aluno.nome,
            medalhas=medalhas_out
        )

    except HTTPException:
        # relança erros 404
        raise
    except Exception as e:
        # encapsula qualquer outro erro num 500 com detalhe
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro interno ao buscar medalhas: {e}"
        )
