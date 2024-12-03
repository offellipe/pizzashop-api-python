from flask import request, jsonify, abort
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from src.models.sqlite.repositories.orders_repository import OrderRepository
from src.models.sqlite.repositories.order_items_repository import OrderItemRepository  # noqa
from src.models.sqlite.repositories.products_repository import ProductRepository  # noqa
from src.authentication import authenticate_user, get_authenticated_user
from src.models.sqlite.settings.connection import db_connection_handler
from src.main.routes.blueprint_routes.orders_bluprint import orders_blueprint


@orders_blueprint.route("/restaurants/<string:restaurant_id>/orders", methods=["POST"])  # noqa
@authenticate_user  # Middleware para autenticação
def create_order(restaurant_id):
    try:
        # Obtém o cliente autenticado
        current_user = get_authenticated_user()
        customer_id = current_user.get("sub")
        if not customer_id:
            abort(401, description="User not authenticated.")

        # Extrair dados do corpo da requisição
        data = request.get_json()
        if not data or "items" not in data:
            abort(400, description="Invalid request body.")

        items = data["items"]

        # Extrair os IDs dos produtos do pedido
        product_ids = [item["productId"] for item in items]

        session: Session = db_connection_handler()

        # Buscar os produtos no banco de dados
        products = session.query(ProductRepository).filter(
            ProductRepository.restaurant_id == restaurant_id,
            ProductRepository.id.in_(product_ids)
        ).all()

        # Validar se todos os produtos existem no restaurante
        available_product_ids = {product.id for product in products}
        for item in items:
            if item["productId"] not in available_product_ids:
                abort(400, description="Not all products are available in this restaurant.")  # noqa

        # Calcular os subtotais e total do pedido
        order_products = []
        total_in_cents = 0

        for item in items:
            product = next(
                product for product in products if product.id == item["productId"]  # noqa
            )
            subtotal = item["quantity"] * product.price_in_cents
            total_in_cents += subtotal

            order_products.append({
                "productId": item["productId"],
                "unitPriceInCents": product.price_in_cents,
                "quantity": item["quantity"],
                "subtotalInCents": subtotal,
            })

        # Criar o pedido e os itens em uma transação
        new_order = OrderRepository(total_in_cents=total_in_cents, customer_id=customer_id, restaurant_id=restaurant_id) # noqa
        session.add(new_order)
        session.flush()  # Garante que o ID do pedido seja gerado

        for order_product in order_products:
            order_item = OrderItemRepository(
                order_id=new_order.id,
                product_id=order_product["productId"],
                price_in_cents=order_product["unitPriceInCents"],
                quantity=order_product["quantity"]
            )
            session.add(order_item)

        session.commit()

        # Retornar o status 201 (Created)
        return jsonify({"orderId": new_order.id}), 201

    except SQLAlchemyError as e:
        # Lidar com erros do banco de dados
        session.rollback()
        return jsonify({"error": str(e)}), 500
    except Exception as e:
        # Lidar com erros genéricos
        return jsonify({"error": str(e)}), 500
