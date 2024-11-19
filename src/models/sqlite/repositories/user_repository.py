from sqlalchemy.orm.exc import NoResultFound
from src.models.sqlite.entities.users import Users
from src.models.sqlite.interfaces.user_repository_interface import (
    UserRepositoryInterface
)


class UserRepository(UserRepositoryInterface):
    def __init__(self, db_connection) -> None:
        self.__db_connection = db_connection

    def insert_user(
            self, name: str, email: str, password: str, role: str
    ) -> None:
        with self.__db_connection as session:
            user = Users(
                name=name,
                email=email,
                password=password,
                role=role,
            )
            session.add(user)
            session.commit()

    def get_user_by_id(self, user_id: int) -> Users:
        with self.__db_connection as session:
            try:
                user = (
                    session
                    .query(Users)
                    .filter(Users.id == user_id)
                    .one()
                )
                return user
            except NoResultFound:
                return None

    def delete_user_by_id(self, user_id: int) -> None:
        with self.__db_connection as session:
            try:
                user = (
                    session
                    .query(Users)
                    .filter(Users.id == user_id)
                    .one()
                )
                session.delete(user)
                session.commit()
            except NoResultFound:
                return None
            except Exception as e:
                session.rollback()
                raise e

    def list_users(self) -> list[Users]:
        with self.__db_connection as session:
            try:
                users = session.query(Users).all()
                return users
            except Exception as e:
                print(f"Erro ao listar usuários: {e}")
                return []
