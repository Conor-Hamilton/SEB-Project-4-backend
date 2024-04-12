from http import HTTPStatus
from functools import wraps
from flask import request, g
import jwt
from app import db
from models.user import UserModel
from config.environment import SECRET


def secure_route(route_func):
    @wraps(route_func)
    def wrapper(*args, **kwargs):
        raw_token = request.headers.get("Authorization")

        if not raw_token:
            return {"message": "Unauthorized"}, HTTPStatus.UNAUTHORIZED
        token = raw_token.replace("Bearer ", "")

        try:
            payload = jwt.decode(token, SECRET, "HS256")
            user_id = payload["sub"]
            user = db.session.get(UserModel, user_id)
            if not user:
                return {"message": "User not found"}, HTTPStatus.UNAUTHORIZED

        except jwt.ExpiredSignatureError:
            return {"message": "Token has expired"}, HTTPStatus.UNAUTHORIZED
        except jwt.InvalidTokenError:
            return {"message": "Invalid token"}, HTTPStatus.UNAUTHORIZED
        except Exception as e:
            print(f"Unexpected error: {e}")
            return {"message": "Unauthorized"}, HTTPStatus.UNAUTHORIZED

    return wrapper
