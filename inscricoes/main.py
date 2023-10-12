from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from inscricoes.db.crud import create_conferencia, read_conferencias
from inscricoes.db.model import Conferencia, Inscricao, Participante, get_sql_engine

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


@app.post("/create_conference")
async def create_conference(conferencia: Conferencia):
    create_conferencia(conferencia)
    return conferencia.dict()
