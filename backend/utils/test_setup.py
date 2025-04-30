# backend/utils/test_setup.py
# backend/utils/test_setup.py

from sqlalchemy.orm import Session  # ✅ Corrigido
from backend.database.models import Aluno

# Função para garantir que um aluno de teste existe
def garantir_aluno_teste(db: Session):
    aluno_existente = db.query(Aluno).filter(Aluno.email == "teste@teste.com").first()
    if aluno_existente:
        return aluno_existente

    aluno_teste = Aluno(
        nome="Aluno Teste",
        email="teste@teste.com",
        senha="1234",
        foto_url="https://link-da-foto.com"
    )
    db.add(aluno_teste)
    db.commit()
    db.refresh(aluno_teste)
    return aluno_teste




