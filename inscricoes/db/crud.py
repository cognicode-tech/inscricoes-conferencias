from sqlmodel import Session, select

from inscricoes.db.model import Conferencia, Inscricao, Participante, get_sql_engine


def create_conferencia(conferencia: Conferencia, engine=None):
    engine = get_sql_engine() if engine is None else engine
    with Session(engine) as session:
        session.add(conferencia)
        session.commit()


def create_inscricao(inscricao: Inscricao, engine=None):
    engine = get_sql_engine() if engine is None else engine
    with Session(engine) as session:
        session.add(inscricao)
        session.commit()


def create_participante(participante: Participante, engine=None):
    engine = get_sql_engine() if engine is None else engine
    with Session(engine) as session:
        session.add(participante)
        session.commit()


def read_conferencia(conferencia_id: int, engine=None):
    engine = get_sql_engine() if engine is None else engine
    with Session(engine) as session:
        return session.get(Conferencia, conferencia_id)


def read_conferencias(engine=None):
    engine = get_sql_engine() if engine is None else engine
    with Session(engine) as session:
        return session.exec(select(Conferencia).order_by(Conferencia.id.desc())).all()


def read_inscricao(inscricao_id: int, engine=None):
    engine = get_sql_engine() if engine is None else engine
    with Session(engine) as session:
        return session.get(Inscricao, inscricao_id)


def read_inscricoes(conferencia_id: int, engine=None):
    engine = get_sql_engine() if engine is None else engine
    with Session(engine) as session:
        return session.exec(
            select(Inscricao).where(Inscricao.conferencia_id == conferencia_id)
        ).all()


def read_participante(participante_id: int, engine=None):
    engine = get_sql_engine() if engine is None else engine
    with Session(engine) as session:
        return session.get(Participante, participante_id)


def read_participantes(inscricao_id: int, engine=None):
    engine = get_sql_engine() if engine is None else engine
    with Session(engine) as session:
        return session.exec(
            select(Participante).where(Participante.inscricao_id == inscricao_id)
        ).all()


def update_conferencia(conferencia_id: int, conferencia: Conferencia, engine=None):
    engine = get_sql_engine() if engine is None else engine
    with Session(engine) as session:
        db_conferencia = session.get(Conferencia, conferencia_id)
        if not db_conferencia:
            return None

        conferencia_data = conferencia.dict(exclude_unset=True)
        for key, value in conferencia_data.items():
            setattr(db_conferencia, key, value)
        session.add(db_conferencia)
        session.commit()
        session.refresh(db_conferencia)


def update_inscricao(inscricao_id: int, inscricao: Inscricao, engine=None):
    engine = get_sql_engine() if engine is None else engine
    with Session(engine) as session:
        db_inscricao = session.get(Inscricao, inscricao_id)
        if not db_inscricao:
            return None

        inscricao_data = inscricao.dict(exclude_unset=True)
        for key, value in inscricao_data.items():
            setattr(db_inscricao, key, value)
        session.add(db_inscricao)
        session.commit()
        session.refresh(db_inscricao)


def update_participante(participante_id: int, participante: Participante, engine=None):
    engine = get_sql_engine() if engine is None else engine
    with Session(engine) as session:
        db_participante = session.get(Participante, participante_id)
        if not db_participante:
            return None

        participante_data = participante.dict(exclude_unset=True)
        for key, value in participante_data.items():
            setattr(db_participante, key, value)
        session.add(db_participante)
        session.commit()
        session.refresh(db_participante)


def delete_conferencia(conferencia_id: int, engine=None):
    engine = get_sql_engine() if engine is None else engine
    with Session(engine) as session:
        session.delete(session.get(Conferencia, conferencia_id))
        session.commit()


def delete_inscricao(inscricao_id, engine=None):
    engine = get_sql_engine() if engine is None else engine
    with Session(engine) as session:
        session.delete(session.get(Inscricao, inscricao_id))
        session.commit()


def delete_participante(participante_id, engine=None):
    engine = get_sql_engine() if engine is None else engine
    with Session(engine) as session:
        session.delete(session.get(Participante, participante_id))
        session.commit()
