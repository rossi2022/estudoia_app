from fastapi import APIRouter
from typing import List

router = APIRouter()

# Exemplo fixo de trecho literário e perguntas
@router.get("/literatura/trecho")
def obter_trecho_literario():
    trecho = (
        "“A liberdade é a possibilidade do isolamento. Se te é impossível viver só, nasceste escravo.”\n"
        "– Fernando Pessoa"
    )

    perguntas = [
        "1. Quem é o autor do trecho?",
        "2. Qual é o tema central abordado na citação?",
        "3. O que o autor relaciona com a liberdade?",
        "4. O trecho expressa uma ideia positiva ou negativa sobre a solidão?",
        "5. Você concorda com a frase? Por quê?"
    ]

    return {
        "trecho": trecho,
        "perguntas": perguntas
    }
from fastapi import APIRouter
from typing import List

router = APIRouter()

# Exemplo fixo de trecho literário e perguntas
@router.get("/literatura/trecho")
def obter_trecho_literario():
    trecho = (
        "“A liberdade é a possibilidade do isolamento. Se te é impossível viver só, nasceste escravo.”\n"
        "– Fernando Pessoa"
    )

    perguntas = [
        "1. Quem é o autor do trecho?",
        "2. Qual é o tema central abordado na citação?",
        "3. O que o autor relaciona com a liberdade?",
        "4. O trecho expressa uma ideia positiva ou negativa sobre a solidão?",
        "5. Você concorda com a frase? Por quê?"
    ]

    return {
        "trecho": trecho,
        "perguntas": perguntas
    }




