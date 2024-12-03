from typing import Dict
from src.models.sqlite.repositories.orders_repository import OrderRepository


class OrdersController:
    def __init__(self, order_repository: OrderRepository) -> None:
        self.__order_repository = order_repository

    def get_orders(self, query_params: Dict, restaurant_id: str, page_index: int = 0) -> Dict: # noqa
        # Extrair parâmetros da query
        order_id = query_params.get("orderId")
        customer_name = query_params.get("customerName")
        status = query_params.get("status")

        # Filtrar os pedidos de acordo com os parâmetros
        orders_count = self.__order_repository.get_orders_count(
            restaurant_id=restaurant_id,
            order_id=order_id,
            status=status,
            customer_name=customer_name
        )

        orders = self.__order_repository.get_orders(
            restaurant_id=restaurant_id,
            order_id=order_id,
            status=status,
            customer_name=customer_name,
            page_index=page_index
        )

        result = {
            "orders": orders,
            "meta": {
                "pageIndex": page_index,
                "perPage": 10,
                "totalCount": orders_count,
            }
        }

        return result

    def get_order_details(self, order_id: int, restaurant_id: str) -> Dict:
        order_details = self.__order_repository.get_order_details(
            order_id=order_id,
            restaurant_id=restaurant_id
        )
        if not order_details:
            return {"error": "Order not found."}
        return order_details
