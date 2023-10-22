from fastapi import APIRouter, Request

from inscricoes.db.crud import create_conferencia, update_conferencia
from inscricoes.db.model import Conferencia
from inscricoes.logger import logger

router = APIRouter()


@router.post("/create_conference")
async def create_conference(conferencia: Conferencia):
    create_conferencia(conferencia)
    return conferencia.dict()


@router.post("/update_conference")
async def update_conference(conferencia: Conferencia):
    conferencia_id = conferencia.id
    update_conferencia(conferencia_id, conferencia)
    return conferencia.dict()
