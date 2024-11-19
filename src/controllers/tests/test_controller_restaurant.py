from types import NoneType
import pytest

from src.controllers.restaurants_controller import RestaurantController
from src.models.sqlite.repositories.restaurant_repository import RestaurantRepository
from src.models.sqlite.settings.connection import db_connection_handler


class MockRestaurant():
    def __init__(self, name, description, manager_id) -> None:
        self.name = name
        self.description = description
        self.manager_id = manager_id


class MockRestaurantRepository:
    def insert_user(self, name: str, email: str, password: str, role: str):
        return {
            "name": name,
            "email": email,
            "password": password,
            "role": role
        }

    def get_user_by_id(self, user_id: int):
        return MockRestaurant(
            name="John",
            email="teste@email.com",
            password="teste",
            role="manager"
        )


class TestUserController:

    def test_create_user(self):
        user_info = {
            "name": "Fellipe",
            "email": "teste@email.com",
            "password": "Teste!@1231",
            "role": "admin"
        }

        controller = RestaurantController(MockRestaurantRepository())
        response = controller.create_user(user_info)

        assert response["data"]["type"] == "User"
        assert response["data"]["count"] == 1
        assert response["data"]["attributes"] == user_info

    def test_invalid_create_user(self):
        user_info = {
            "name": "Fellipe",
            "password": "BRibeiroFKA!@1401",
            "role": "admin"
        }

        controller = UserController(MockRestaurantRepository())
        with pytest.raises(Exception):
            controller.create_user(user_info)

    def test_get_user_by_id(self):
        user_id = 6

        controller = UserController(MockRestaurantRepository())

        user = controller.get_user_by_id(user_id=user_id)

        assert user.name == "John"
        assert user.email == "teste@email.com"
        assert user.role == "manager"

    @pytest.mark.skip(reason="Interação com o banco")
    def test_delete_user_by_id(self):
        restaurant_id = 3

        controller = RestaurantController(
            RestaurantRepository(db_connection_handler)
        )

        controller.delete_restaurant_by_id(restaurant_id=restaurant_id)

        list_user = controller.list_users()

        assert isinstance(list_user, NoneType)

    @pytest.mark.skip(reason="Interação com o banco")
    def test_list_users(self):
        controller = UserController(UserRepository(db_connection_handler))

        list_users = controller.list_users()

        assert len(list_users) == 5
