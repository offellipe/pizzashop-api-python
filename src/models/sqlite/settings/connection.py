from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


class DBConnectionHandler:
    def __init__(self) -> None:
        self.__connection_string = "sqlite:///pizzadb.db"
        self.__engine = create_engine(
            self.__connection_string, connect_args={"check_same_thread": False}
        )
        self.__Session = sessionmaker(bind=self.__engine)
        self.session = None

    def get_engine(self):
        return self.__engine

    def __enter__(self):
        self.session = self.__Session()
        return self.session  # Retorna a sessão diretamente

    def __exit__(self, exc_type, exc_val, exc_tb):
        try:
            if exc_type is not None:
                self.session.rollback()  # Reverte a transação em caso de erro
        finally:
            self.session.close()


db_connection_handler = DBConnectionHandler()
