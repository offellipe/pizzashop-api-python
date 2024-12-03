from flask import jsonify
from src.models.sqlite.repositories.orders_repository import OrderRepository
from src.controllers.metrics_controller import MetricsController
from src.main.routes.blueprint_routes.metrics_blueprint import metrics_blueprint # noqa


@metrics_blueprint.route("/metrics/popular-products/<string:restaurant_id>", methods=["GET"]) # noqa
def get_popular_products(restaurant_id):
    try:
        # Criar uma instância do controlador
        metrics_controller = MetricsController(OrderRepository)

        # Chama o método para obter os produtos populares
        result = metrics_controller.get_popular_products(restaurant_id)

        # Retorna os produtos populares como resposta
        return jsonify(result), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
