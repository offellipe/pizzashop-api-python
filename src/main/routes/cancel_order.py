from flask import jsonify, abort
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from src.models.sqlite.repositories.orders_repository import OrderRepository
from src.authentication import authenticate_user, get_managed_restaurant_id
from src.models.sqlite.settings.connection import db_connection_handler
from src.main.routes.blueprint_routes.orders_bluprint import orders_blueprint


@orders_blueprint.route("/orders/<string:order_id>/cancel", methods=["PATCH"])
@authenticate_user  # Middleware para autenticação
def cancel_order(order_id):
    try:
        # Obtém o restaurante gerenciado pelo usuário autenticado
        restaurant_id = get_managed_restaurant_id()

        if not restaurant_id:
            abort(401, description="User is not a restaurant manager.")  # Unauthorized # noqa

        # Verificar se o pedido pertence ao restaurante gerenciado
        session: Session = db_connection_handler()
        order = session.query(OrderRepository).filter(
            OrderRepository.id == order_id,
            OrderRepository.restaurant_id == restaurant_id
        ).first()

        if not order:
            abort(401, description="Order not found under the user managed restaurant.")  # Unauthorized # noqa

        # Verificar o status do pedido
        if order.status not in ["pending", "processing"]:
            return jsonify({
                "code": "STATUS_NOT_VALID",
                "message": "O pedido não pode ser cancelado depois de ser enviado." # noqa
            }), 400

        # Atualizar o status do pedido para 'canceled'
        order.status = "canceled"
        session.commit()

        # Retornar status 204 (No Content)
        return "", 204

    except SQLAlchemyError as e:
        # Lidar com erros do banco de dados
        session.rollback()
        return jsonify({"error": str(e)}), 500
    except Exception as e:
        # Lidar com erros genéricos
        return jsonify({"error": str(e)}), 500
