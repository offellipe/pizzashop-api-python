from abc import ABC, abstractmethod
from typing import List
from src.models.sqlite.entities.orders import Orders


class OrderRepositoryInterface(ABC):
    @abstractmethod
    def insert_order(
        self,
        customer_id: str,
        restaurant_id: str,
        status: str,
        total_in_cents: int
    ) -> None:
        pass

    @abstractmethod
    def get_order_by_id(self, order_id: int) -> Orders:
        pass

    @abstractmethod
    def delete_order_by_id(self, order_id: int) -> None:
        pass

    @abstractmethod
    def list_orders(self) -> List[Orders]:
        pass

    @abstractmethod
    def update_order_status(self, order_id: int, new_status: str) -> None:
        pass

    @abstractmethod
    def get_orders_by_restaurant(self, restaurant_id: str) -> List[Orders]:
        pass
