from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


class DBConnectionHanlder:
    def __init__(self) -> None:
        self.__connection_string = "sqlite:///pizzadb.db"
        self.__engine = None
        self.session = None

    def connect_to_db(self):
        self.__engine = create_engine(self.__connection_string)

    def get_engine(self):
        return self.__engine

    def __enter__(self):
        if not self.__engine:
            raise RuntimeError("Database engine is not initialized. Call 'connect_to_db' first.") # noqa

        Session = sessionmaker(bind=self.__engine)  # Bind the engine to the sessionmaker # noqa
        self.session = Session()  # Create a session instance
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.session.close()


db_connection_handler = DBConnectionHanlder()
