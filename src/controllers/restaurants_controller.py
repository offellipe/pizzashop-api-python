from typing import Dict

from src.controllers.interfaces.restaurant_controller_inteface import (
    RestaurantControllerInterface
)
from src.models.sqlite.repositories.restaurant_repository import (
    RestaurantRepository
)


class RestaurantController(RestaurantControllerInterface):
    def __init__(self, restaurant_repository: RestaurantRepository) -> None:
        self.__restaurant_repository = restaurant_repository

    def create_restaurant(self, restaurant_info: Dict) -> Dict:
        name = restaurant_info["name"]
        description = restaurant_info["description"]
        manager_id = restaurant_info["manager_id"]

        self.__insert_restaurant_in_db(name, description, manager_id)
        formated_response = self.__format_response(restaurant_info)
        return formated_response

    def get_restaurant_by_id(self, restaurant_id: int):
        restaurant = self.__restaurant_repository.get_restaurant_by_id(
            restaurant_id=restaurant_id
        )
        return restaurant

    def delete_restaurant_by_id(self, restaurant_id: int) -> None:
        self.__restaurant_repository.delete_restaurant_by_id(
            restaurant_id=restaurant_id
        )

    def list_restaurants(self) -> list:
        return self.__restaurant_repository.list_restaurants()

    def __insert_restaurant_in_db(
        self, name: str, description: str, manager_id: int,
    ) -> None:

        self.__restaurant_repository.insert_user(name, description, manager_id)

    def __format_response(self, restaurant_dict: Dict) -> Dict:
        return {
            "data": {
                "type": "Restaurant",
                "count": 1,
                "attributes": restaurant_dict
            }
        }
