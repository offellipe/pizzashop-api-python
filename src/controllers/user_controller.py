from typing import Dict
from src.controllers.interfaces.user_controller_inteface import (
    UserControllerInterface
)
from src.models.sqlite.repositories.user_repository import UserRepository


class UserController(UserControllerInterface):
    def __init__(self, user_repository: UserRepository) -> None:
        self.__user_repository = user_repository

    def create_user(self, user_info: Dict) -> Dict:
        name = user_info["name"]
        email = user_info["email"]
        password = user_info["password"]
        role = user_info["role"]

        self.__insert_person_in_db(name, email, password, role)
        formated_response = self.__format_response(user_info)
        return formated_response

    def get_user_by_id(self, user_id: int):
        user = self.__user_repository.get_user_by_id(user_id=user_id)
        return user

    def delete_user_by_id(self, user_id: int) -> None:
        self.__user_repository.delete_user_by_id(user_id=user_id)

    def list_users(self) -> list:
        return self.__user_repository.list_users()

    def __insert_person_in_db(
            self, name: str, email: str, password: str, role: str
    ) -> None:

        self.__user_repository.insert_user(name, email, password, role)

    def __format_response(self, user_dic: Dict) -> Dict:
        return {
            "data": {
                "type": "User",
                "count": 1,
                "attributes": user_dic
            }
        }
