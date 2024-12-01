from flask import request, abort


def authenticate_user(func):
    def wrapper(*args, **kwargs):
        # Verificar se o token está presente no cabeçalho da requisição
        token = request.headers.get("Authorization")
        if not token or not is_valid_token(token):
            abort(401, description="Unauthorized")
        return func(*args, **kwargs)
    return wrapper


def is_valid_token(token):
    # Lógica para validar o token
    return True
