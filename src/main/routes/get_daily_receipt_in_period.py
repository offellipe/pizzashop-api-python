from flask import request, jsonify
from datetime import datetime, timedelta
from src.authentication import authenticate_user, get_managed_restaurant_id
from src.models.sqlite.repositories.orders_repository import OrderRepository
from src.models.sqlite.settings.connection import db_connection_handler
from src.main.routes.blueprint_routes.metrics_blueprint import metrics_blueprint # noqa


@metrics_blueprint.route("/metrics/daily-receipt-in-period", methods=["GET"])
@authenticate_user
def get_daily_receipt_in_period():
    try:
        restaurant_id = get_managed_restaurant_id()
        if not restaurant_id:
            return jsonify({"error": "Unauthorized"}), 403

        query_params = request.args
        from_date = query_params.get("from")
        to_date = query_params.get("to")

        start_date = (
            datetime.strptime(from_date, "%Y-%m-%d") if from_date else datetime.now() - timedelta(days=7) # noqa
        )
        end_date = (
            datetime.strptime(to_date, "%Y-%m-%d") if to_date else start_date + timedelta(days=7) # noqa
        )

        if (end_date - start_date).days > 7:
            return (
                jsonify({
                    "code": "INVALID_PERIOD",
                    "message": "O intervalo das datas não pode ser superior a 7 dias." # noqa
                }),
                400,
            )

        with db_connection_handler() as session:  # Manage the DB session
            order_repository = OrderRepository(session)

            # Use repository method to fetch data
            receipt_per_day = order_repository.get_daily_receipt_in_period(
                restaurant_id, start_date, end_date
            )

        return jsonify(receipt_per_day), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
