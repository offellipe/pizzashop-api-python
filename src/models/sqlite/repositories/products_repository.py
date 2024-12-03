from sqlalchemy.orm.exc import NoResultFound
from src.models.sqlite.entities.products import Products


class ProductRepository:
    def __init__(self, db_connection) -> None:
        self.__db_connection = db_connection

    def insert_product(
        self,
        product_id: str,
        name: str,
        description: str,
        price_in_cents: int,
        restaurant_id: str
    ) -> None:
        """
        Insere um novo produto no banco de dados.
        """
        with self.__db_connection as session:
            try:
                product = Products(
                    id=product_id,
                    name=name,
                    description=description,
                    price_in_cents=price_in_cents,
                    restaurant_id=restaurant_id,
                )
                session.add(product)
                session.commit()
            except Exception as e:
                session.rollback()
                raise e

    def get_product_by_id(self, product_id: str) -> Products:
        """
        Recupera um produto pelo ID.
        """
        with self.__db_connection as session:
            try:
                product = (
                    session.query(Products)
                    .filter(Products.id == product_id)
                    .one()
                )
                return product
            except NoResultFound:
                return None
            except Exception as e:
                raise e

    def delete_product_by_id(self, product_id: str) -> None:
        """
        Deleta um produto pelo ID.
        """
        with self.__db_connection as session:
            try:
                product = (
                    session.query(Products)
                    .filter(Products.id == product_id)
                    .one()
                )
                session.delete(product)
                session.commit()
            except NoResultFound:
                return None
            except Exception as e:
                session.rollback()
                raise e

    def list_products_by_restaurant(self, restaurant_id: str) -> list[Products]: # noqa
        """
        Lista todos os produtos de um restaurante.
        """
        with self.__db_connection as session:
            try:
                products = (
                    session.query(Products)
                    .filter(Products.restaurant_id == restaurant_id)
                    .all()
                )
                return products
            except Exception as e:
                print(f"Erro ao listar produtos: {e}")
                return []

    def update_product(
        self,
        product_id: str,
        name: str = None,
        description: str = None,
        price_in_cents: int = None
    ) -> None:
        """
        Atualiza as informações de um produto.
        """
        with self.__db_connection as session:
            try:
                product = (
                    session.query(Products)
                    .filter(Products.id == product_id)
                    .one()
                )
                if product:
                    if name is not None:
                        product.name = name
                    if description is not None:
                        product.description = description
                    if price_in_cents is not None:
                        product.price_in_cents = price_in_cents
                    session.commit()
            except NoResultFound:
                return None
            except Exception as e:
                session.rollback()
                raise e

    def get_products_by_ids_and_restaurant(
        self, product_ids: list[str], restaurant_id: str
    ) -> list[Products]:
        """
        Recupera produtos por IDs e valida se pertencem a um restaurante específico. # noqa
        """
        with self.__db_connection as session:
            try:
                products = (
                    session.query(Products)
                    .filter(
                        Products.id.in_(product_ids),
                        Products.restaurant_id == restaurant_id,
                    )
                    .all()
                )
                return products
            except Exception as e:
                print(f"Erro ao buscar produtos: {e}")
                return []
