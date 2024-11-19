from abc import ABC, abstractmethod
from src.models.sqlite.entities.users import Users


class UserRepositoryInterface(ABC):

    @abstractmethod
    def insert_user(
        self, name: str, email: str, password: int, role: str
    ) -> None:
        pass

    @abstractmethod
    def get_user_by_id(self, user_id: int) -> Users:
        pass

    @abstractmethod
    def delete_user_by_id(self, user_id: int) -> None:
        pass

    @abstractmethod
    def list_users(self) -> list[Users]:
        pass
