from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from backend.db import SessionLocal
from backend.database.models import Aluno, Professor

SECRET_KEY = "seu_segredo_super_secreto"  # ✅ troque por variável de ambiente depois
ALGORITHM = "HS256"

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
bearer_scheme = HTTPBearer()

def get_password_hash(password):
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def criar_token(dados: dict):
    return jwt.encode(dados, SECRET_KEY, algorithm=ALGORITHM)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme), db: Session = Depends(get_db)):
    token = credentials.credentials
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = int(payload.get("sub"))
        tipo = payload.get("tipo")  # 👈 tipo: aluno ou professor
        if not user_id or not tipo:
            raise HTTPException(status_code=401, detail="Token inválido")
    except JWTError:
        raise HTTPException(status_code=401, detail="Token inválido")

    if tipo == "aluno":
        user = db.query(Aluno).filter(Aluno.id == user_id).first()
    elif tipo == "professor":
        user = db.query(Professor).filter(Professor.id == user_id).first()
    else:
        raise HTTPException(status_code=401, detail="Tipo de usuário inválido")

    if user is None:
        raise HTTPException(status_code=401, detail="Usuário não encontrado")
    return user

