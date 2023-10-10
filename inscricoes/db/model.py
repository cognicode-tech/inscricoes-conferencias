from datetime import datetime
from typing import Optional

from sqlmodel import Field, SQLModel, create_engine

from inscricoes.settings import DB_ENGINE_URL


def get_sql_engine(engine_url: str | None = None, db_name: str = "inscricoes"):
    engine_url = DB_ENGINE_URL if engine_url is None else engine_url
    engine = create_engine(engine_url, echo=True)
    SQLModel.metadata.create_all(engine)

    return engine


class Participante(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nome: str
    idade: int
    sexo: str
    isento: bool
    tipo_inscricao: str
    valor_inscricao: float
    inscricao_id: int = Field(foreign_key="inscricao.id")


class Conferencia(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nome: str
    data: str
    local: str


class Inscricao(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    conferencia_id: int = Field(foreign_key="conferencia.id")
    cidade: str
    estado: str
    responsavel: str
    data: datetime = Field(default=datetime.now())
    pg_total: Optional[float] = Field(default=0.0)
    pg_dinheiro: Optional[float] = Field(default=0.0)
    pg_cheque: Optional[float] = Field(default=0.0)
    pg_cartao: Optional[float] = Field(default=0.0)
    pg_transferencia: Optional[float] = Field(default=0.0)
    pg_deposito: Optional[float] = Field(default=0.0)
    pg_pendencias: Optional[float] = Field(default=0.0)
    observacoes: Optional[str] = Field(default="")
