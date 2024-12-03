from flask import request, jsonify
from src.models.sqlite.repositories.orders_repository import OrderRepository
from src.controllers.orders_controller import OrdersController
from src.main.routes.blueprint_routes.orders_bluprint import orders_blueprint


# Instanciando o repositório e o controlador
orders_controller = OrdersController(OrderRepository) # noqa


# Rota que usa restaurant_id como path parameter
@orders_blueprint.route("/orders/<string:restaurant_id>", methods=["GET"])
def get_orders(restaurant_id):
    try:
        # Obtendo parâmetros da query string
        query_params = request.args
        page_index = query_params.get("pageIndex", type=int, default=0)

        # Criar uma instância do controlador para processar a lógica
        orders_controller = OrdersController(OrderRepository)

        # Chama o método para obter os pedidos
        result = orders_controller.get_orders(query_params, restaurant_id, page_index) # noqa

        return jsonify(result), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
