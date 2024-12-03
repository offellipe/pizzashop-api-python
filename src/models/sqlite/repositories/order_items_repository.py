from sqlalchemy.orm.exc import NoResultFound
from src.models.sqlite.entities.orders_items import OrderItems


class OrderItemRepository:
    def __init__(self, db_connection) -> None:
        self.__db_connection = db_connection

    def insert_order_item(
        self,
        order_item_id: str,
        order_id: str,
        product_id: str,
        quantity: int,
        price_in_cents: int
    ) -> None:
        """
        Insere um novo item de pedido no banco de dados.
        """
        with self.__db_connection as session:
            try:
                order_item = OrderItems(
                    id=order_item_id,
                    order_id=order_id,
                    product_id=product_id,
                    quantity=quantity,
                    price_in_cents=price_in_cents,
                )
                session.add(order_item)
                session.commit()
            except Exception as e:
                session.rollback()
                raise e

    def get_order_item_by_id(self, order_item_id: str) -> OrderItems:
        """
        Recupera um item de pedido pelo ID.
        """
        with self.__db_connection as session:
            try:
                order_item = (
                    session.query(OrderItems)
                    .filter(OrderItems.id == order_item_id)
                    .one()
                )
                return order_item
            except NoResultFound:
                return None
            except Exception as e:
                raise e

    def delete_order_item_by_id(self, order_item_id: str) -> None:
        """
        Deleta um item de pedido pelo ID.
        """
        with self.__db_connection as session:
            try:
                order_item = (
                    session.query(OrderItems)
                    .filter(OrderItems.id == order_item_id)
                    .one()
                )
                session.delete(order_item)
                session.commit()
            except NoResultFound:
                return None
            except Exception as e:
                session.rollback()
                raise e

    def list_order_items_by_order(self, order_id: str) -> list[OrderItems]:
        """
        Lista todos os itens de um pedido específico.
        """
        with self.__db_connection as session:
            try:
                order_items = (
                    session.query(OrderItems)
                    .filter(OrderItems.order_id == order_id)
                    .all()
                )
                return order_items
            except Exception as e:
                print(f"Erro ao listar itens do pedido: {e}")
                return []

    def update_order_item(
        self,
        order_item_id: str,
        quantity: int = None,
        price_in_cents: int = None
    ) -> None:
        """
        Atualiza as informações de um item de pedido.
        """
        with self.__db_connection as session:
            try:
                order_item = (
                    session.query(OrderItems)
                    .filter(OrderItems.id == order_item_id)
                    .one()
                )
                if order_item:
                    if quantity is not None:
                        order_item.quantity = quantity
                    if price_in_cents is not None:
                        order_item.price_in_cents = price_in_cents
                    session.commit()
            except NoResultFound:
                return None
            except Exception as e:
                session.rollback()
                raise e

    def get_order_items_by_order_and_product(
        self, order_id: str, product_id: str
    ) -> OrderItems:
        """
        Recupera um item de pedido específico pelo pedido e ID do produto.
        """
        with self.__db_connection as session:
            try:
                order_item = (
                    session.query(OrderItems)
                    .filter(
                        OrderItems.order_id == order_id,
                        OrderItems.product_id == product_id,
                    )
                    .one()
                )
                return order_item
            except NoResultFound:
                return None
            except Exception as e:
                raise e
