from http import HTTPStatus
import logging
import jwt
from datetime import datetime, timezone, timedelta
from flask import Blueprint, request
from marshmallow.exceptions import ValidationError
from config.environment import SECRET
from app import db
from models.user import UserModel
from serializers.user import UserSerializer

user_serializer = UserSerializer()


router = Blueprint("users", __name__)


@router.route("/signup", methods=["POST"])
def signup():

    try:
        user_dictionary = request.json
        user_model = user_serializer.load(user_dictionary)

        db.session.add(user_model)
        db.session.commit()
        return user_serializer.jsonify(user_model)

    except ValidationError as e:
        return {
            "errors": e.messages,
            "message": "Something went wrong",
        }, HTTPStatus.UNPROCESSABLE_ENTITY
    except Exception as e:
        logging.exception("An error occurred during signup.")
        return {"message": "Something went wrong"}, HTTPStatus.INTERNAL_SERVER_ERROR


@router.route("/login", methods=["POST"])
def login():
    now_utc = datetime.now(timezone.utc)
    credentials_dictionary = request.json
    user = (
        db.session.query(UserModel)
        .filter_by(email=credentials_dictionary["email"])
        .first()
    )

    if not user or not user.validate_password(credentials_dictionary.get("password")):
        return {"message": "Login failed. Try again."}, 401

    payload = {
        "exp": now_utc + timedelta(days=2),
        "iat": now_utc,
        "sub": user.id,
    }

    token = jwt.encode(payload, SECRET, algorithm="HS256")

    return {"message": "Login successful", "token": token}
