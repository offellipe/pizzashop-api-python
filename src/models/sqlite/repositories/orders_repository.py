import datetime
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy import func, and_
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

    def get_daily_receipt_in_period(self, restaurant_id: str, start_date: datetime, end_date: datetime): # noqa
        try:
            results = (
                self.__db_connection.query(
                    datetime.strftime("%d/%m", Orders.created_at).label("date"), # noqa
                    datetime.sum(Orders.total_in_cents).label("receipt"),
                )
                .filter(
                    and_(
                        Orders.restaurant_id == restaurant_id,
                        Orders.created_at >= start_date,
                        Orders.created_at <= end_date,
                    )
                )
                .group_by(func.strftime("%d/%m", Orders.created_at))
                .having(func.sum(Orders.total_in_cents) >= 1)
                .order_by(func.strftime("%d/%m", Orders.created_at))
                .all()
            )

            return [{"date": r.date, "receipt": int(r.receipt)} for r in results] # noqa

        except Exception as e:
            raise Exception(f"Error fetching daily receipts: {e}")

    def get_orders_per_day(self, restaurant_id: str, start_date: datetime):
        try:
            results = (
                self.__db_connection.query(
                    func.strftime("%Y-%m-%d", Orders.created_at).label("dayWithMonthAndYear"), # noqa
                    func.count(Orders.id).label("amount"),
                )
                .filter(
                    and_(
                        Orders.restaurant_id == restaurant_id,
                        Orders.created_at >= start_date,
                    )
                )
                .group_by(func.strftime("%Y-%m-%d", Orders.created_at))
                .having(func.count(Orders.id) >= 1)
                .all()
            )

            return [{"dayWithMonthAndYear": r.dayWithMonthAndYear, "amount": r.amount} for r in results] # noqa

        except Exception as e:
            raise Exception(f"Error fetching orders per day: {e}")

    def get_order_details(self, restaurant_id, order_id):
        # Lógica para consultar o banco de dados, incluindo joins com clientes, itens de pedido e produtos # noqa
        order = self.session.query(Orders).filter(
            Orders.id == order_id,
            Orders.restaurant_id == restaurant_id
        ).first()

        if order:
            # Aqui você pode incluir joins ou subconsultas para carregar informações de cliente, itens de pedido, etc. # noqa
            return {
                "id": order.id,
                "createdAt": order.created_at,
                "status": order.status,
                "totalInCents": order.total_in_cents,
                "customer": {
                    "name": order.customer.name,
                    "phone": order.customer.phone,
                    "email": order.customer.email,
                },
                "orderItems": [
                    {
                        "id": item.id,
                        "priceInCents": item.price_in_cents,
                        "quantity": item.quantity,
                        "product": {
                            "name": item.product.name,
                        }
                    }
                    for item in order.items
                ]
            }
        return None

    def get_orders(self, query_params, restaurant_id: str, page_index: int):
        # Lógica para obter os pedidos, agora utilizando o restaurant_id
        order_id = query_params.get("orderId")
        customer_name = query_params.get("customerName")
        status = query_params.get("status")

        # Aqui é onde você chama o repositório de pedidos
        orders = self.__order_repository.get_orders_by_restaurant(restaurant_id) # noqa

        # Filtro adicional com base nos parâmetros de consulta
        if order_id:
            orders = [order for order in orders if order.id == order_id]
        if customer_name:
            orders = [order for order in orders if customer_name.lower() in order.customer.name.lower()] # noqa
        if status:
            orders = [order for order in orders if order.status == status]

        # Paginação
        per_page = 10
        total_orders = len(orders)
        start_index = page_index * per_page
        end_index = start_index + per_page
        orders_to_return = orders[start_index:end_index]

        # Resposta formatada
        result = {
            "orders": orders_to_return,
            "meta": {
                "pageIndex": page_index,
                "perPage": per_page,
                "totalCount": total_orders,
            }
        }

        return result
