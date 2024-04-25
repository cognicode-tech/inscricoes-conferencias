from typing import Optional
from sqlmodel import SQLModel, Field, create_engine, Session

from inscricoes.settings import DB_ENGINE_URL

def get_sql_engine(engine_url: str | None = None, db_name: str = "inscricoes"):
    engine_url = DB_ENGINE_URL if engine_url is None else engine_url
    engine = create_engine(engine_url, echo=False)
    SQLModel.metadata.create_all(engine)
    return engine

class Conferencia(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nome: str
    data: str
    local: str

def create_conferencia(conferencia: Conferencia, engine=None):
    engine = get_sql_engine() if engine is None else engine
    with Session(engine) as session:
        conferencia = Conferencia(nome=conferencia[0],data=conferencia[1],local=conferencia[2])
        session.add(conferencia)
        session.commit()
        session.refresh(conferencia)


# teste manual:
#conferencia = "Conferencia 1", "24/04/2024", "Castanhal"
#print(conferencia[0], conferencia[1], conferencia[2])
#create_conferencia(conferencia)