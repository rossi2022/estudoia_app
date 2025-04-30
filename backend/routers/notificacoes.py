from fastapi import APIRouter
import random

router = APIRouter()

@router.get("/notificacoes/lembrete")
def lembrete_diario():
    return {
        "mensagem": "Não se esqueça de estudar hoje! 📚 Reserve 30 minutos para revisar o que aprendeu. Você consegue! 💪"
    }

@router.get("/notificacoes/motivacional")
def mensagem_motivacional():
    mensagens = [
        "Você é capaz de ir além do que imagina! 🚀",
        "Cada esforço conta. Continue avançando! 🌟",
        "A jornada do conhecimento começa com um passo. Dê o seu hoje! 📘",
        "Orgulhe-se de cada pequena conquista! 🏅",
        "Estudar agora é plantar sucesso para o futuro! 🌱"
    ]
    return {"mensagem": random.choice(mensagens)}

