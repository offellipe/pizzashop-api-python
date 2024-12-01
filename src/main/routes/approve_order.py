from flask import Blueprint, jsonify, abort
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from src.models.sqlite.repositories.orders_repository import OrderRepository
from src.authentication import authenticate_user, get_managed_restaurant_id
from src.models.sqlite.settings.connection import db_connection_handler

# Criar um blueprint para as rotas de pedidos
orders_blueprint = Blueprint("orders", __name__)


@orders_blueprint.route("/orders/<string:order_id>/approve", methods=["PATCH"])
@authenticate_user  # Middleware para autenticação
def approve_order(order_id):
    try:
        # Obtém o restaurante gerenciado pelo usuário autenticado
        restaurant_id = get_managed_restaurant_id()

        # Verificar se o pedido pertence ao restaurante gerenciado
        session: Session = db_connection_handler()
        order = session.query(OrderRepository).filter(
                OrderRepository.id == order_id,
                OrderRepository.restaurant_id == restaurant_id,
        ).first()

        if not order:
            abort(403, description="Unauthorized")  # Lançar erro 403 se o pedido não existir ou não pertencer # noqa

        # Verificar o status do pedido
        if order.status != "pending":
            return jsonify({"message": "Order was already approved before."}), 400 # noqa

        # Atualizar o status do pedido para 'processing'
        order.status = "processing"
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
