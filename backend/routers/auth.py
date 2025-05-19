from fastapi import APIRouter, HTTPException, status, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from jose import jwt
from datetime import datetime, timedelta
from backend.db import get_db
from backend.database.models import Aluno
from backend.utils.security import verify_password, criar_token

# =============================
# 🔹 Inicialização do roteador
# =============================
router = APIRouter(
    prefix="/auth",
    tags=["Autenticação"]
)

# =============================
# 🔸 Schemas de entrada e saída
# =============================
class LoginData(BaseModel):
    email: str
    senha: str

class LoginResponse(BaseModel):
    message: str
    aluno_id: int
    nome: str
    token: str

# =============================
# 🔸 Endpoint de login
# =============================
@router.post("/login", response_model=LoginResponse)
def login(data: LoginData, db: Session = Depends(get_db)):
    aluno = db.query(Aluno).filter(Aluno.email == data.email).first()

    # 🔍 Prints de debug colocados dentro da função
    print("📥 Senha digitada:", data.senha)
    print("🔒 Senha no banco:", aluno.senha if aluno else "Nenhum aluno")
    print("✅ Comparação:", verify_password(data.senha, aluno.senha) if aluno else "Aluno inexistente")

    if not aluno or not verify_password(data.senha, aluno.senha):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciais inválidas"
        )

    token = criar_token({
        "sub": aluno.id,
        "tipo": "aluno"
    })

    return {
        "message": "Login bem-sucedido",
        "aluno_id": aluno.id,
        "nome": aluno.nome,
        "token": token
    }





























