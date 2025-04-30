# backend/routers/timeline.py

from fastapi import APIRouter, Query
from pydantic import BaseModel
from typing import List

router = APIRouter()

class Evento(BaseModel):
    data: str
    descricao: str

@router.get("/timeline/", response_model=List[Evento])
def gerar_timeline(periodo: str = Query(..., description="Informe o período desejado")):
    periodo = periodo.lower()

    eventos = []

    if "século xviii" in periodo or "1700" in periodo:
        eventos.append(Evento(data="1776", descricao="Independência dos Estados Unidos"))
        eventos.append(Evento(data="1789", descricao="Revolução Francesa"))
        eventos.append(Evento(data="1799", descricao="Golpe de 18 de Brumário de Napoleão"))

    elif "século xx" in periodo or "1900" in periodo:
        eventos.append(Evento(data="1914", descricao="Início da Primeira Guerra Mundial"))
        eventos.append(Evento(data="1939", descricao="Início da Segunda Guerra Mundial"))
        eventos.append(Evento(data="1969", descricao="Chegada do homem à Lua"))

    else:
        eventos.append(Evento(data="0000", descricao="Período informado não encontrado."))

    return eventos





