from flask import request, jsonify
from sqlalchemy.exc import SQLAlchemyError
from src.authentication import authenticate_user, get_current_user
from src.models.sqlite.repositories.evaluation_repository import EvaluationRepository # noqa
from src.models.sqlite.settings.connection import db_connection_handler
from src.main.routes.blueprint_routes.evaluations_blueprint import evaluations_blueprint # noqa


@evaluations_blueprint.route("/evaluations", methods=["GET"])
@authenticate_user
def get_evaluations():
    try:
        # Obter informações do usuário atual
        user = get_current_user()
        restaurant_id = user.get("restaurantId")

        if not restaurant_id:
            return jsonify({"error": "User is not a restaurant manager."}), 401

        # Obter o índice da página a partir dos parâmetros de consulta
        page_index = request.args.get("pageIndex", 0, type=int)
        offset = page_index * 10
        limit = 10

        with db_connection_handler() as session:
            evaluation_repository = EvaluationRepository(session)
            evaluations = evaluation_repository.get_evaluations(restaurant_id, offset, limit) # noqa

        return jsonify(evaluations), 200

    except SQLAlchemyError as e:
        return jsonify({"error": str(e)}), 500
