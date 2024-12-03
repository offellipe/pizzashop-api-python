from flask import Flask
from flask_cors import CORS
from src.models.sqlite.settings.connection import db_connection_handler

# importar blueprints
from src.main.routes.blueprint_routes.evaluations_blueprint import evaluations_blueprint # noqa
from src.main.routes.blueprint_routes.restaurants_blueprint import restaurants_blueprint # noqa
from src.main.routes.blueprint_routes.metrics_blueprint import metrics_blueprint # noqa
from src.main.routes.blueprint_routes.orders_bluprint import orders_blueprint

db_connection_handler.connect_to_db()

app = Flask(__name__)
CORS(app)

app.register_blueprint(evaluations_blueprint)
app.register_blueprint(restaurants_blueprint)
app.register_blueprint(metrics_blueprint)
app.register_blueprint(orders_blueprint)
