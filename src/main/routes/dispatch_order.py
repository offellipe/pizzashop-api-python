from flask import jsonify, abort
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from src.models.sqlite.repositories.orders_repository import OrderRepository
from src.authentication import authenticate_user, get_managed_restaurant_id
from src.models.sqlite.settings.connection import db_connection_handler
from src.main.routes.blueprint_routes.orders_bluprint import orders_blueprint


@orders_blueprint.route("/orders/<string:order_id>/dispatch", methods=["PATCH"]) # noqa
@authenticate_user  # Middleware para autenticação
def dispatch_order(order_id):
    """
    Marca um pedido como 'delivering'.
    """
    try:
        # Obter o restaurante gerenciado pelo usuário autenticado
        restaurant_id = get_managed_restaurant_id()
        if not restaurant_id:
            abort(403, description="Unauthorized: No managed restaurant found.") # noqa

        # Verificar se o pedido existe e pertence ao restaurante
        session: Session = db_connection_handler()
        order_repo = OrderRepository(session)
        order = order_repo.get_order_by_id(order_id)

        if not order or order.restaurant_id != restaurant_id:
            abort(403, description="Unauthorized: Order not found or access denied.") # noqa

        # Verificar o status do pedido
        if order.status != "processing":
            return jsonify({"message": "O pedido já foi enviado ao cliente."}), 400 # noqa

        # Atualizar o status do pedido para 'delivering'
        order_repo.update_order_status(order_id, "delivering")

        # Retornar status 204 (No Content)
        return "", 204

    except SQLAlchemyError as e:
        # Lidar com erros do banco de dados
        session.rollback()
        return jsonify({"error": str(e)}), 500
    except Exception as e:
        # Lidar com erros genéricos
        return jsonify({"error": str(e)}), 500
