from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from inscricoes.db.crud import delete_conferencia, read_conferencia, read_conferencias
from inscricoes.db.model import Conferencia, Inscricao, Participante, get_sql_engine
from inscricoes.logger import logger
from inscricoes.routes import pages
from inscricoes.routes.api import conferences_api

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
app.include_router(pages.router, tags=["pages"])
app.include_router(conferences_api.router, prefix="/api", tags=["api"])
