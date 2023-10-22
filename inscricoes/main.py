from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from inscricoes.db.crud import (
    create_conferencia,
    delete_conferencia,
    read_conferencia,
    read_conferencias,
    update_conferencia,
)
from inscricoes.db.model import Conferencia, Inscricao, Participante, get_sql_engine
from inscricoes.logger import logger

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def list_conferences(request: Request):
    conferencias = read_conferencias()
    return templates.TemplateResponse(
        "home/lista-conferencias.html",
        {"request": request, "conferencias": conferencias},
    )


@app.get("/nova-conferencia")
async def new_conference(request: Request):
    return templates.TemplateResponse(
        "home/nova-conferencia.html",
        {"request": request},
    )


@app.delete("/delete/{objeto}/{objeto_id}")
async def delete_object(objeto: str, objeto_id: int):
    if objeto == "inscricao":
        pass  # delete_inscricao(objeto_id)
    elif objeto == "participante":
        pass  # delete_participante(objeto_id)
    elif objeto == "conferencia":
        # FIXME: Tem que remover as inscrições e participantes da conferência
        delete_conferencia(objeto_id)
        return {"message": "{objeto} {id} excluído com sucesso"}


@app.get("/update")
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


# Actions
@app.post("/create_conference")
async def create_conference(conferencia: Conferencia):
    create_conferencia(conferencia)
    return conferencia.dict()


@app.post("/update_conference")
async def update_conference(conferencia: Conferencia):
    conferencia_id = conferencia.id
    update_conferencia(conferencia_id, conferencia)
    return conferencia.dict()
