from sqlalchemy import func
from src.models.sqlite.repositories.orders_repository import OrderRepository
from src.models.sqlite.entities.orders import Orders
from src.models.sqlite.entities.orders_items import OrderItems
from src.models.sqlite.entities.products import Products


class MetricsController:
    def __init__(self, order_repository: OrderRepository):
        self.__order_repository = order_repository

    def get_popular_products(self, restaurant_id: str):
        try:
            # Realizando a consulta para obter os produtos mais populares
            popular_products = (
                self.__order_repository.__db_connection.query(
                    Products.name.label("product"),
                    func.count(OrderItems.id).label("amount")
                )
                .join(OrderItems, OrderItems.product_id == Products.id)
                .join(Orders, Orders.id == OrderItems.order_id)
                .filter(Orders.restaurant_id == restaurant_id)
                .group_by(Products.name)
                .order_by(func.count(OrderItems.id).desc())
                .limit(5)
                .all()
            )

            # Retornar os produtos populares
            return [{"product": p.product, "amount": p.amount} for p in popular_products] # noqa
        except Exception as e:
            print(f"Error fetching popular products: {e}")
            return []
