from flask import Blueprint, jsonify

# Definindo o Blueprint
api = Blueprint("api", __name__)


@api.route("/")
def home():
    return jsonify({"message": "Welcome to the API!"})


def register_routes(app):
    app.register_blueprint(api)
