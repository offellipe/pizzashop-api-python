from flask import jsonify
from src.authentication import authenticate_user, get_current_user
from src.models.sqlite.repositories.orders_repository import OrderRepository
from src.models.sqlite.settings.connection import db_connection_handler
from src.errors import UnauthorizedError, NotAManagerError
from src.main.routes.blueprint_routes.orders_bluprint import orders_blueprint


@orders_blueprint.route("/orders/<order_id>", methods=["GET"])
@authenticate_user
def get_order_details(order_id):
    try:
        current_user = get_current_user()
        restaurant_id = current_user.get("restaurantId")

        if not restaurant_id:
            raise NotAManagerError()

        with db_connection_handler() as session:
            order_repository = OrderRepository(session)

            # Use repository method to fetch order details
            order = order_repository.get_order_details(restaurant_id, order_id)

        if not order:
            raise UnauthorizedError()

        return jsonify(order), 200

    except UnauthorizedError:
        return jsonify({"error": "Unauthorized"}), 401
    except NotAManagerError:
        return jsonify({"error": "User is not a restaurant manager"}), 403
    except Exception as e:
        return jsonify({"error": str(e)}), 500
