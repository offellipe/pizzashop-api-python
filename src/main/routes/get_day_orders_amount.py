from flask import jsonify
from datetime import datetime, timedelta
from src.authentication import authenticate_user, get_managed_restaurant_id
from src.models.sqlite.repositories.orders_repository import OrderRepository
from src.models.sqlite.settings.connection import db_connection_handler
from src.main.routes.blueprint_routes.metrics_blueprint import metrics_blueprint # noqa


@metrics_blueprint.route("/metrics/day-orders-amount", methods=["GET"])
@authenticate_user
def get_day_orders_amount():
    try:
        restaurant_id = get_managed_restaurant_id()
        if not restaurant_id:
            return jsonify({"error": "Unauthorized"}), 403

        today = datetime.now()
        yesterday = today - timedelta(days=1)

        today_with_month_and_year = today.strftime('%Y-%m-%d')
        yesterday_with_month_and_year = yesterday.strftime('%Y-%m-%d')

        start_of_yesterday = datetime.combine(yesterday, datetime.min.time())

        with db_connection_handler() as session:
            order_repository = OrderRepository(session)

            # Use repository method to fetch data
            orders_per_day = order_repository.get_orders_per_day(restaurant_id, start_of_yesterday) # noqa

        today_orders_amount = next(
            (order for order in orders_per_day if order["dayWithMonthAndYear"] == today_with_month_and_year), # noqa
            None,
        )
        yesterday_orders_amount = next(
            (order for order in orders_per_day if order["dayWithMonthAndYear"] == yesterday_with_month_and_year), # noqa
            None,
        )

        diff_from_yesterday = (
            (today_orders_amount["amount"] * 100) / yesterday_orders_amount["amount"] # noqa
            if today_orders_amount and yesterday_orders_amount
            else None
        )

        return jsonify({
            "amount": today_orders_amount["amount"] if today_orders_amount else 0, # noqa
            "diffFromYesterday": round(diff_from_yesterday - 100, 2) if diff_from_yesterday else 0 # noqa
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
