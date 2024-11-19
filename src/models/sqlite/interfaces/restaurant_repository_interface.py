from abc import ABC, abstractmethod
from src.models.sqlite.entities.restaurants import Restaurants


class RestaurantRepositoryInterface(ABC):

    @abstractmethod
    def insert_restaurant(
        self, name: str, description: str, manager_id: int
    ) -> None:
        pass

    @abstractmethod
    def get_restaurant_by_id(self, restaurant_id: int) -> Restaurants:
        pass

    @abstractmethod
    def delete_restaurant_by_id(self, restaurant_id: int) -> None:
        pass

    @abstractmethod
    def list_restaurants(self) -> list[Restaurants]:
        pass
