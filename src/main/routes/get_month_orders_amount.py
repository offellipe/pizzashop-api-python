from flask import jsonify
from datetime import datetime, timedelta
from src.authentication import authenticate_user, get_managed_restaurant_id
from src.models.sqlite.repositories.orders_repository import OrderRepository
from src.models.sqlite.settings.connection import db_connection_handler
from src.main.routes.blueprint_routes.metrics_blueprint import metrics_blueprint # noqa


@metrics_blueprint.route("/metrics/month-orders-amount", methods=["GET"])
@authenticate_user
def get_month_orders_amount():
    try:
        restaurant_id = get_managed_restaurant_id()
        if not restaurant_id:
            return jsonify({"error": "Unauthorized"}), 403

        today = datetime.now()
        last_month = today - timedelta(days=30)
        start_of_last_month = datetime(last_month.year, last_month.month, 1)

        last_month_with_year = last_month.strftime('%Y-%m')
        current_month_with_year = today.strftime('%Y-%m')

        with db_connection_handler() as session:
            order_repository = OrderRepository(session)

            # Use repository method to fetch data
            orders_per_month = order_repository.get_orders_per_month(
                restaurant_id, start_of_last_month
            )

        current_month_orders_amount = next(
            (order for order in orders_per_month if order["monthWithYear"] == current_month_with_year), # noqa
            None
        )
        last_month_orders_amount = next(
            (order for order in orders_per_month if order["monthWithYear"] == last_month_with_year), # noqa
            None
        )

        diff_from_last_month = (
            (current_month_orders_amount["amount"] * 100) / last_month_orders_amount["amount"] # noqa
            if current_month_orders_amount and last_month_orders_amount
            else None
        )

        return jsonify({
            "amount": current_month_orders_amount["amount"] if current_month_orders_amount else 0, # noqa
            "diffFromLastMonth": round(diff_from_last_month - 100, 2) if diff_from_last_month else 0 # noqa
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
