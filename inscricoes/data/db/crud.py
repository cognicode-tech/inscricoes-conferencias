from sqlmodel import Session, select

from inscricoes.data.db.model import get_sql_engine, Conferencia, Inscricao, Participante
from inscricoes.data.logger import logger

# ---------------------------------- CONFERENCIA SECTION ----------------------------------- #]

def create_conferencia(conferencia: dict, engine=None):
    engine = get_sql_engine() if engine is None else engine
    with Session(engine) as session:
        conferencia_obj = Conferencia(nome=conferencia['name'], data=conferencia['date'], local=conferencia['city'])
        session.add(conferencia_obj)
        session.commit()
        session.refresh(conferencia_obj)

    logger.info(f"Conferencia {conferencia_obj.id} criada com os dados: {conferencia_obj}")

def read_single_conference(conferencia_id: int, engine=None):
    engine = get_sql_engine() if engine is None else engine
    with Session(engine) as session:
        return session.get(Conferencia, conferencia_id)

def read_multiple_conferences(engine=None):
    engine = get_sql_engine() if engine is None else engine
    with Session(engine) as session:
        return session.exec(select(Conferencia).order_by(Conferencia.id.desc())).all()

def delete_conferencia(conferencia_id: int, engine=None):
    engine = get_sql_engine() if engine is None else engine
    with Session(engine) as session:
        session.delete(session.get(Conferencia, conferencia_id))
        session.commit()
        
    logger.info(f"Conferência {conferencia_id} deletada com sucesso.")

def update_conferencia(conferencia_id: int, conferencia_update: dict, engine=None):
    engine = get_sql_engine() if engine is None else engine
    with Session(engine) as session:
        conferencia = session.get(Conferencia, conferencia_id)
        conferencia.nome = conferencia_update['name']
        conferencia.data = conferencia_update['date']
        conferencia.local = conferencia_update['city']
        session.commit()
    
    logger.info(f"Conferência {conferencia_id} atualizada com sucesso.")

# ---------------------------------- INSCRICAO SECTION ----------------------------------- #
def create_participante(participante: dict, engine=None):
    engine = get_sql_engine() if engine is None else engine
    print(participante,'\n\n')
    with Session(engine) as session:
        session.add(Participante(nome=participante['name'],idade=int(participante['age']),sexo=participante['gender'],
                                 tipo_inscricao=participante['pay_type'],valor_inscricao=float(participante['pay_value']),
                                 isento=participante['isento'],inscricao_id=int(participante['inscricao_id'])))
        session.commit()

# ---------------------------------- INSCRICAO ----------------------------------- #            
def create_inscricao(inscricao: dict, engine=None):
    engine = get_sql_engine() if engine is None else engine
    print('\n\n',inscricao,'\n\n')
    with Session(engine) as session:
        session.add(Inscricao(conferencia_id=inscricao['conference_id'],responsavel=inscricao['responsable'],cidade=inscricao['city'],
                              estado=inscricao['estate'],pg_dinheiro=inscricao['pay_paper'],pg_deposito=inscricao['pay_deposit'],
                              pg_transferencia=inscricao['pay_transfer'],pg_cheque=inscricao['pay_check'], observacoes=inscricao['observations'],
                              pg_total=inscricao['total_pay']))
        session.commit()

def read_inscricao_id(engine=None):
    engine = get_sql_engine() if engine is None else engine
    with Session(engine) as session:
        last_inscricao = session.scalar(select(Inscricao).order_by(Inscricao.id.desc()).limit(1))
        if last_inscricao:
            return last_inscricao.id
        else:
            return None
               
def read_inscricao(inscricao_id: int, engine=None):
    engine = get_sql_engine() if engine is None else engine
    with Session(engine) as session:
        return session.get(Inscricao, inscricao_id)
           
def read_inscricoes(conferencia_id, engine=None):
    engine = get_sql_engine() if engine is None else engine
    with Session(engine) as session:
        return session.exec(select(Inscricao).where(Inscricao.conferencia_id == conferencia_id)).all()