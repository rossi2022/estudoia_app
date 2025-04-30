from fastapi import APIRouter, HTTPException, status
from backend.schemas import QuizRequest, QuizResponse, PerguntaQuiz
from backend.ai_module import gerar_quiz

router = APIRouter(prefix="/quiz", tags=["Quiz"])

@router.post("/", response_model=QuizResponse, status_code=status.HTTP_200_OK)
def criar_quiz(req: QuizRequest):
    if req.quantidade < 1 or req.quantidade > 20:
        raise HTTPException(400, "Quantidade deve ser entre 1 e 20")
    raw = gerar_quiz(req.materia, req.assunto, req.quantidade)
    # raw deve ser List[dict] com keys enunciado, opcoes e resposta_correta
    perguntas = [PerguntaQuiz(**q) for q in raw]
    return QuizResponse(perguntas=perguntas)
