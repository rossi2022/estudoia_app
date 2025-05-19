# File: backend/routers/professores.py

from fastapi import APIRouter, HTTPException, Depends, UploadFile, File, Form, status
from sqlalchemy.orm import Session
from backend.db import get_db
from backend.database.models import Professor, Aluno, NotaMensal
from backend.schemas import ProfessorLogin, ProfessorOut
from backend.utils.security import verify_password, criar_token, get_current_user
from passlib.context import CryptContext
import os
import shutil

router = APIRouter(
    prefix="/professores",
    tags=["professores"]
)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@router.post(
    "/cadastro",
    response_model=ProfessorOut,
    status_code=status.HTTP_201_CREATED
)
async def cadastrar_professor(
    nome: str = Form(...),
    email: str = Form(...),
    senha: str = Form(...),
    foto: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    # Verifica e-mail duplicado
    if db.query(Professor).filter_by(email=email).first():
        raise HTTPException(status_code=409, detail="Email já cadastrado.")

    # Salva imagem no disco
    pasta = "frontend/static/img/professores"
    os.makedirs(pasta, exist_ok=True)
    nome_arquivo = f"{email.replace('@','_at_').replace('.','_')}.jpg"
    caminho = os.path.join(pasta, nome_arquivo)
    with open(caminho, "wb") as f:
        shutil.copyfileobj(foto.file, f)

    # Hash da senha
    senha_hash = pwd_context.hash(senha)

    # Cria e retorna o professor
    professor = Professor(
        nome=nome,
        email=email,
        senha=senha_hash,
        foto_url=f"/static/img/professores/{nome_arquivo}"
    )
    db.add(professor)
    db.commit()
    db.refresh(professor)
    return professor

@router.post("/login")
def login_professor(
    dados: ProfessorLogin,
    db: Session = Depends(get_db)
):
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

@router.get("/alunos")
def listar_alunos(
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    if user.__class__.__name__ != "Professor":
        raise HTTPException(status_code=403, detail="Acesso restrito a professores")
    alunos = db.query(Aluno).all()
    return [{"id": a.id, "nome": a.nome, "email": a.email} for a in alunos]

@router.get("/media-desempenho")
def media_por_materia(
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    if user.__class__.__name__ != "Professor":
        raise HTTPException(status_code=403, detail="Acesso restrito a professores")

    rows = db.query(NotaMensal.materia, NotaMensal.nota).all()
    if not rows:
        return {}

    resultados = {}
    for materia, nota in rows:
        resultados.setdefault(materia, []).append(nota)

    medias = {
        materia: round(sum(notas) / len(notas), 2)
        for materia, notas in resultados.items()
    }
    return medias
