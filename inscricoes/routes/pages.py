from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from inscricoes import routes
from inscricoes.db.crud import delete_conferencia, read_conferencia, read_conferencias

router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get("/", response_class=HTMLResponse)
async def list_conferences(request: Request):
    conferencias = read_conferencias()
    return templates.TemplateResponse(
        "home/lista-conferencias.html",
        {"request": request, "conferencias": conferencias},
    )


@router.get("/nova-conferencia")
async def new_conference(request: Request):
    return templates.TemplateResponse(
        "home/nova-conferencia.html",
        {"request": request},
    )


@router.delete("/delete/{objeto}/{objeto_id}")
async def delete_object(objeto: str, objeto_id: int):
    if objeto == "inscricao":
        pass  # delete_inscricao(objeto_id)
    elif objeto == "participante":
        pass  # delete_participante(objeto_id)
    elif objeto == "conferencia":
        # FIXME: Tem que remover as inscrições e participantes da conferência
        delete_conferencia(objeto_id)
        return {"message": "{objeto} {id} excluído com sucesso"}


@router.get("/update")
async def update_object(objeto: str, objeto_id: int, request: Request):
    if objeto == "inscricao":
        pass  # delete_inscricao(objeto_id)
    elif objeto == "participante":
        pass  # delete_participante(objeto_id)
    elif objeto == "conferencia":
        conferencia = read_conferencia(objeto_id)

        return templates.TemplateResponse(
            "home/atualiza-conferencia.html",
            {"request": request, "conferencia": conferencia},
        )
