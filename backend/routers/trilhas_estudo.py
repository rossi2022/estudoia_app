from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from backend.db import get_db
from backend.database.models import TrilhaAprendizado
from backend.schemas import TrilhaAprendizadoOut
from datetime import date

router = APIRouter(prefix="/trilhas-estudo", tags=["Trilhas de Estudo"])

@router.get("/{aluno_id}", response_model=list[TrilhaAprendizadoOut])
def sugerir_trilhas_personalizadas(aluno_id: int, db: Session = Depends(get_db)):
    hoje = date.today()

    trilhas = [
        TrilhaAprendizadoOut(
            id=1,
            aluno_id=aluno_id,
            titulo="Leitura sobre Revolução Francesa",
            descricao="Leia um resumo e responda 3 perguntas",
            habilidade="Interpretação histórica",
            status="pendente",
            data_criacao=hoje,
        ),
        TrilhaAprendizadoOut(
            id=2,
            aluno_id=aluno_id,
            titulo="Resumo manuscrito sobre ecossistemas",
            descricao="Escreva um resumo de 10 linhas sobre o tema",
            habilidade="Escrita e síntese",
            status="pendente",
            data_criacao=hoje,
        ),
        TrilhaAprendizadoOut(
            id=3,
            aluno_id=aluno_id,
            titulo="Vídeo sobre equações do 1º grau",
            descricao="Assista ao vídeo e resolva 3 questões",
            habilidade="Resolução de problemas",
            status="pendente",
            data_criacao=hoje,
        ),
        TrilhaAprendizadoOut(
            id=4,
            aluno_id=aluno_id,
            titulo="Mini-prova: Interpretação de texto",
            descricao="Faça uma mini-avaliação com 3 perguntas",
            habilidade="Leitura crítica",
            status="pendente",
            data_criacao=hoje,
        ),
    ]
    return trilhas


