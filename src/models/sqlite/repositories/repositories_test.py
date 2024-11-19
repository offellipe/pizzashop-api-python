import pytest
from src.models.sqlite.settings.connection import db_connection_handler
from .pets_repository import PetsRepository
from .user_repository import UserRepository

db_connection_handler.connect_to_db()


def test_list_users():
    repo = PetsRepository(db_connection_handler)
    response = repo.list_pets()
    print()
    print(response)


# @pytest.mark.skip(reason="interacao com o banco")
def test_delete_pet():
    name = "belinha"

    repo = PetsRepository(db_connection_handler)
    repo.delete_pets(name)


# @pytest.mark.skip(reason="interacao com o banco")
def test_insert_user():
    name = "Fellipe"
    last_name = "test last"
    age = 77
    pet_id = 2

    repo = UserRepository(db_connection_handler)
    repo.insert_user(first_name, last_name, age, pet_id)


# @pytest.mark.skip(reason="interacao com o banco")
def test_get_person():
    person_id = 1

    repo = UserRepository(db_connection_handler)
    response = repo.get_user_by_id(person_id)
    print()
    print(response)
    print(response.pet_name)
