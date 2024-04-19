from http import HTTPStatus
import logging
import jwt
from datetime import datetime, timezone, timedelta
from flask import Blueprint, request, g
from marshmallow.exceptions import ValidationError
from config.environment import SECRET
from app import db
from models.user import UserModel
from models.userType import UserType
from serializers.userSchema import UserSerializer
from middleware.secureRoute import secure_route
from flask import jsonify

user_serializer = UserSerializer()
users_controller = Blueprint("users", __name__)


# Get Current User Details
@users_controller.route("/user", methods=["GET"])
@secure_route
def get_current_user():
    user = g.current_user
    return user_serializer.jsonify(user), HTTPStatus.OK


@users_controller.route("/users", methods=["GET"])
@secure_route
def get_all_users():
    if not g.current_user.is_admin:
        return {"message": "Unauthorized"}, HTTPStatus.UNAUTHORIZED

    users = UserModel.query.all()
    return (
        user_serializer.jsonify(users, many=True),
        HTTPStatus.OK,
    )


# Creating a User
@users_controller.route("/signup", methods=["POST"])
def signup():
    user_dictionary = request.get_json()

    if user_dictionary["password"] != user_dictionary.get("confirmPassword"):
        return {
            "errors": {"confirmPassword": ["Passwords do not match"]},
            "messages": "Passwords do not match",
        }, HTTPStatus.UNPROCESSABLE_ENTITY

    del user_dictionary["confirmPassword"]

    try:

        user_serializer = UserSerializer()
        user = user_serializer.load(user_dictionary)

        customer_type = UserType.query.filter_by(name="Customer").first()
        if not customer_type:
            raise Exception("Customer user type not found")

        user.user_types.append(customer_type)

        db.session.add(user)
        db.session.commit()

        return user_serializer.jsonify(user), HTTPStatus.CREATED
    except ValidationError as e:

        return {
            "errors": e.messages,
            "messages": "Something went wrong during validation",
        }, HTTPStatus.UNPROCESSABLE_ENTITY


# Login a User
@users_controller.route("/login", methods=["POST"])
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

    payload = {"exp": now_utc + timedelta(days=2), "iat": now_utc, "sub": user.id}
    token = jwt.encode(payload, SECRET, algorithm="HS256")
    return {"message": "Login successful", "token": token}


# Update User Details
@users_controller.route("/users/<int:user_id>", methods=["PUT"])
@secure_route
def update_user(user_id):
    if g.current_user.id != user_id and not g.current_user.is_admin:
        return {"message": "Unauthorized"}, HTTPStatus.UNAUTHORIZED
    user = UserModel.query.get_or_404(user_id)
    user_data = request.get_json()
    user = user_serializer.load(user_data, instance=user, partial=True)
    db.session.commit()
    return user_serializer.jsonify(user), HTTPStatus.OK


# Delete a User
@users_controller.route("/users/<int:user_id>", methods=["DELETE"])
@secure_route
def delete_user(user_id):
    if g.current_user.id != user_id and not g.current_user.is_admin:
        return {"message": "Unauthorized"}, HTTPStatus.UNAUTHORIZED
    user = UserModel.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return "", HTTPStatus.NO_CONTENT
