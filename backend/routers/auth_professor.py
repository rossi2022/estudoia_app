# File: backend/routers/auth_professor.py

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from backend.db import get_db
from backend.database.models import Professor, Aluno, NotaMensal
from backend.schemas import ProfessorLogin, ProfessorOut
from backend.utils.security import verify_password, criar_token, get_current_user

router = APIRouter()

@router.post("/professores/login")
def login_professor(dados: ProfessorLogin, db: Session = Depends(get_db)):
    professor = db.query(Professor).filter(Professor.email == dados.email).first()
    if not professor or not verify_password(dados.senha, professor.senha):
        raise HTTPException(status_code=401, detail="Credenciais inválidas")

    token = criar_token({"sub": str(professor.id), "tipo": "professor"})
    return {
        "message": "Login realizado com sucesso",
        "token": token,
        "professor_id": professor.id,
        "nome": professor.nome
    }

@router.get("/professores/alunos")
def listar_alunos(db: Session = Depends(get_db), user=Depends(get_current_user)):
    if user.__class__.__name__ != "Professor":
        raise HTTPException(status_code=403, detail="Acesso restrito a professores")
    
    alunos = db.query(Aluno).all()
    return [{"id": a.id, "nome": a.nome, "email": a.email} for a in alunos]

@router.get("/professores/media-desempenho")
def media_por_materia(db: Session = Depends(get_db), user=Depends(get_current_user)):
    if user.__class__.__name__ != "Professor":
        raise HTTPException(status_code=403, detail="Acesso restrito a professores")

    resultados = {}
    rows = db.query(NotaMensal.materia, NotaMensal.nota).all()

    if not rows:
        return {}

    for materia, nota in rows:
        if materia not in resultados:
            resultados[materia] = []
        resultados[materia].append(nota)

    medias = {materia: round(sum(notas) / len(notas), 2) for materia, notas in resultados.items()}
    return medias
