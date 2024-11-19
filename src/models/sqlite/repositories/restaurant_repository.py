from sqlalchemy.orm.exc import NoResultFound
from src.models.sqlite.entities.restaurants import Restaurants
from src.models.sqlite.interfaces.restaurant_repository_interface import (
    RestaurantRepositoryInterface
)


class RestaurantRepository(RestaurantRepositoryInterface):
    def __init__(self, db_connection) -> None:
        self.__db_connection = db_connection

    def insert_restaurant(
        self, name: str, description: str, manager_id: int
    ) -> None:
        with self.__db_connection as session:
            restaunt = Restaurants(
                name=name,
                description=description,
                manager_id=manager_id
            )
            session.add(restaunt)
            session.commit()

    def get_restaurant_by_id(self, restaurant_id: int) -> Restaurants:
        with self.__db_connection as session:
            try:
                restaurant = (
                    session
                    .query(Restaurants)
                    .filter(Restaurants.id == restaurant_id)
                    .one()
                )
                return restaurant
            except NoResultFound:
                return None

    def delete_restaurant_by_id(self, restaurant_id: int) -> None:
        with self.__db_connection as session:
            try:
                restaurant = (
                    session
                    .query(Restaurants)
                    .filter(Restaurants.id == restaurant_id)
                    .one()
                )
                session.delete(restaurant)
                session.commit()
            except NoResultFound:
                return None
            except Exception as e:
                session.rollback()
                raise e

    def list_restaurants(self) -> list[Restaurants]:
        with self.__db_connection as session:
            try:
                users = session.query(Restaurants).all()
                return users
            except Exception as e:
                print(f"Erro ao listar restaurantes: {e}")
                return []
