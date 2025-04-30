# backend/routers/professores.py

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from backend.db import get_db
from backend.database.models import Professor

router = APIRouter(
    prefix="/professores",
    tags=["Professores"]
)

# 📚 Cadastro de Professor
@router.post("/cadastro")
def cadastrar_professor(nome: str, email: str, senha: str, db: Session = Depends(get_db)):
    # Verifica se já existe professor com mesmo e-mail
    existing_professor = db.query(Professor).filter(Professor.email == email).first()
    if existing_professor:
        raise HTTPException(status_code=400, detail="Email já cadastrado.")

    novo_professor = Professor(nome=nome, email=email, senha=senha)
    db.add(novo_professor)
    db.commit()
    db.refresh(novo_professor)

    return {"mensagem": "Professor cadastrado com sucesso!", "id": novo_professor.id}


# 🔐 Login de Professor
@router.post("/login")
def login_professor(email: str, senha: str, db: Session = Depends(get_db)):
    professor = db.query(Professor).filter(Professor.email == email, Professor.senha == senha).first()

    if not professor:
        raise HTTPException(status_code=401, detail="Email ou senha inválidos.")

    return {"mensagem": "Login realizado com sucesso!", "professor_id": professor.id, "nome": professor.nome}
