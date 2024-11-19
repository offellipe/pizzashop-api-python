from typing import Dict
from abc import ABC, abstractmethod


class UserControllerInterface(ABC):

    @abstractmethod
    def create_user(self, user_info: Dict) -> Dict:
        pass

    @abstractmethod
    def get_user_by_id(self, user_id: int):
        pass

    @abstractmethod
    def delete_user_by_id(self, user_id: int) -> None:
        pass

    @abstractmethod
    def list_users(self) -> list:
        pass
