from sqlalchemy.orm.exc import NoResultFound
from src.models.sqlite.entities.orders import Orders
from src.models.sqlite.interfaces.order_repository_interface import (
    OrderRepositoryInterface
)


class OrderRepository(OrderRepositoryInterface):
    def __init__(self, db_connection) -> None:
        self.__db_connection = db_connection

    def insert_order(
        self,
        customer_id: str,
        restaurant_id: str,
        status: str = "pending",
        total_in_cents: int = 0,
    ) -> None:
        with self.__db_connection as session:
            try:
                order = Orders(
                    customer_id=customer_id,
                    restaurant_id=restaurant_id,
                    status=status,
                    total_in_cents=total_in_cents,
                )
                session.add(order)
                session.commit()
            except Exception as e:
                session.rollback()
                raise e

    def get_order_by_id(self, order_id: int) -> Orders:
        with self.__db_connection as session:
            try:
                order = (
                    session
                    .query(Orders)
                    .filter(Orders.id == order_id)
                    .one()
                )
                return order
            except NoResultFound:
                return None

    def delete_order_by_id(self, order_id: int) -> None:
        with self.__db_connection as session:
            try:
                order = (
                    session
                    .query(Orders)
                    .filter(Orders.id == order_id)
                    .one()
                )
                session.delete(order)
                session.commit()
            except NoResultFound:
                return None
            except Exception as e:
                session.rollback()
                raise e

    def list_orders(self) -> list[Orders]:
        with self.__db_connection as session:
            try:
                orders = session.query(Orders).all()
                return orders
            except Exception as e:
                print(f"Erro ao listar pedidos: {e}")
                return []

    def update_order_status(self, order_id: int, new_status: str) -> None:
        with self.__db_connection as session:
            try:
                order = (
                    session
                    .query(Orders)
                    .filter(Orders.id == order_id)
                    .one()
                )
                if order:
                    order.status = new_status
                    session.commit()
            except NoResultFound:
                return None
            except Exception as e:
                session.rollback()
                raise e

    def get_orders_by_restaurant(self, restaurant_id: str) -> list[Orders]:
        with self.__db_connection as session:
            try:
                orders = (
                    session
                    .query(Orders)
                    .filter(Orders.restaurant_id == restaurant_id)
                    .all()
                )
                return orders
            except Exception as e:
                print(f"Erro ao buscar pedidos por restaurante: {e}")
                return []
