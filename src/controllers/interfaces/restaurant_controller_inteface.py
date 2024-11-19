from typing import Dict
from abc import ABC, abstractmethod


class RestaurantControllerInterface(ABC):

    @abstractmethod
    def create_restaurant(self, restaurant_info: Dict) -> Dict:
        pass

    @abstractmethod
    def get_restaurant_by_id(self, restaurant_id: int):
        pass

    @abstractmethod
    def delete_restaurant_by_id(self, restaurant_id: int) -> None:
        pass

    @abstractmethod
    def list_restaurants(self) -> list:
        pass
