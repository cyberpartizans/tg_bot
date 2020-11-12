from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from settings import DB_PARAMS
from .models import meta


def get_meta():
    return meta


def get_db():
    db_string = f"{DB_PARAMS['prefix']}://" \
                f"{DB_PARAMS['user']}:{DB_PARAMS['pass']}@" \
                f"{DB_PARAMS['host']}:{DB_PARAMS['port']}/{DB_PARAMS['db_name']}"
    db = create_engine(db_string)
    return db


# session for transactions
def get_db_session(db):
    session_class = sessionmaker(db)
    session = session_class()
    return session


def create_db_structure():
    db = get_db()
    m = get_meta()
    get_db_session(db)
    m.create_all(db)
