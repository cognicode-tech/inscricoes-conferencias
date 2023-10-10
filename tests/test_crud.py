import pytest
from sqlmodel import Session, create_engine

from inscricoes.db.crud import (
    create_conferencia,
    create_inscricao,
    create_participante,
    delete_conferencia,
    delete_inscricao,
    delete_participante,
    read_conferencia,
    read_inscricao,
    read_participante,
    update_conferencia,
    update_inscricao,
    update_participante,
)
from inscricoes.db.model import Conferencia, Inscricao, Participante, get_sql_engine


# Setup a test database
@pytest.fixture(scope="session")
def db_engine():
    engine = get_sql_engine(engine_url="sqlite:///:memory:")
    yield engine
    engine.dispose()


@pytest.fixture(scope="session")
def test_data():
    return {
        "conferencia": Conferencia(
            nome="Test Conference", data="2022-12-12", local="Test Location"
        ),
        "inscricao": Inscricao(
            conferencia_id=1,
            cidade="Test City",
            estado="Test State",
            responsavel="Test Responsible",
        ),
        "participante": Participante(
            nome="Test Participant",
            idade=30,
            sexo="M",
            isento=False,
            tipo_inscricao="Test Type",
            valor_inscricao=100.0,
            inscricao_id=1,
        ),
    }


# Tests for Conferencia
def test_create_conferencia(db_engine, test_data):
    create_conferencia(test_data["conferencia"], engine=db_engine)
    result = read_conferencia(1, db_engine)
    assert result.nome == "Test Conference"


def test_read_conferencia(db_engine):
    result = read_conferencia(1, db_engine)
    assert result.nome == "Test Conference"


def test_update_conferencia(db_engine, test_data):
    test_conferencia = test_data["conferencia"]
    test_conferencia.nome = "Updated Conference"
    update_conferencia(1, test_conferencia, db_engine)
    result = read_conferencia(1, db_engine)
    assert result.nome == "Updated Conference"


def test_delete_conferencia(db_engine):
    delete_conferencia(1, db_engine)
    result = read_conferencia(1, db_engine)
    assert result is None


# Tests for Inscricao
def test_create_inscricao(db_engine, test_data):
    create_inscricao(test_data["inscricao"], engine=db_engine)
    result = read_inscricao(1, db_engine)
    assert result.cidade == "Test City"


def test_read_inscricao(db_engine):
    result = read_inscricao(1, db_engine)
    assert result.responsavel == "Test Responsible"


def test_update_inscricao(db_engine, test_data):
    test_inscricao = test_data["inscricao"]
    test_inscricao.cidade = "Updated City"
    update_inscricao(1, test_inscricao, db_engine)
    result = read_inscricao(1, db_engine)
    assert result.cidade == "Updated City"


def test_delete_inscricao(db_engine):
    delete_inscricao(1, db_engine)
    result = read_inscricao(1, db_engine)
    assert result is None


# Tests for Inscricao
def test_create_participante(db_engine, test_data):
    create_participante(test_data["participante"], engine=db_engine)
    result = read_participante(1, db_engine)
    assert result.nome == "Test Participant"


def test_read_participante(db_engine):
    result = read_participante(1, db_engine)
    assert result.nome == "Test Participant"


def test_update_participante(db_engine, test_data):
    test_participante = test_data["participante"]
    test_participante.nome = "Updated Participant"
    update_participante(1, test_participante, db_engine)
    result = read_participante(1, db_engine)
    assert result.nome == "Updated Participant"


def test_delete_participante(db_engine):
    delete_participante(1, db_engine)
    result = read_participante(1, db_engine)
    assert result is None
