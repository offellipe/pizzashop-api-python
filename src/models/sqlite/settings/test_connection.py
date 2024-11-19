from sqlalchemy.engine import Engine
from src.models.sqlite.settings.connection import DBConnectionHandler


def test_connect_to_db():
    local_db_handler = DBConnectionHandler()

    local_db_handler.connect_to_db()
    db_engine = local_db_handler.get_engine()

    assert db_engine is not None, "O motor do banco de dados não foi inicializado."
    assert isinstance(db_engine, Engine), "O objeto retornado não é uma instância de Engine do SQLAlchemy."
