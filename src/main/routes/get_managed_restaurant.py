from flask import jsonify
from src.authentication import authenticate_user, get_managed_restaurant_id
from src.models.sqlite.repositories.restaurant_repository import RestaurantRepository # noqa
from src.models.sqlite.settings.connection import db_connection_handler
from src.main.routes.blueprint_routes.restaurants_blueprint import restaurants_blueprint # noqa


@restaurants_blueprint.route("/managed-restaurant", methods=["GET"])
@authenticate_user
def get_managed_restaurant():
    try:
        # Obtém o ID do restaurante gerido pelo usuário autenticado
        restaurant_id = get_managed_restaurant_id()
        if not restaurant_id:
            return jsonify({"error": "Unauthorized"}), 403

        # Conecta ao banco de dados e utiliza o repositório para buscar o restaurante  # noqa
        with db_connection_handler() as session:
            restaurant_repository = RestaurantRepository(session)
            restaurant = restaurant_repository.get_restaurant_by_id(restaurant_id)  # noqa

        # Verifica se o restaurante foi encontrado
        if not restaurant:
            return jsonify({"error": "Restaurant not found."}), 404

        # Retorna o restaurante encontrado
        return jsonify(restaurant.to_dict()), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
