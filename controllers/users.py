from http import HTTPStatus
import logging
import jwt
from datetime import datetime, timezone, timedelta
from flask import Blueprint, request, g, jsonify
from flask_cors import cross_origin
from marshmallow.exceptions import ValidationError
from config.environment import SECRET
from app import db
from models.user import UserModel
from models.userType import UserType
from serializers.userSchema import UserSerializer
from middleware.secureRoute import secure_route
from sqlalchemy.exc import IntegrityError

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
            "message": "Passwords do not match",
        }, 422

    del user_dictionary["confirmPassword"]

    try:
        user_serializer = UserSerializer()
        user = user_serializer.load(user_dictionary)

        existing_email_user = UserModel.query.filter_by(email=user.email).first()
        existing_username_user = UserModel.query.filter_by(
            username=user.username
        ).first()

        errors = {}
        if existing_email_user:
            errors["email"] = ["Email address already exists"]
        if existing_username_user:
            errors["username"] = ["Username already exists"]

        if errors:
            return {"errors": errors, "message": "User already exists"}, 422

        customer_type = UserType.query.filter_by(name="Customer").first()
        if not customer_type:
            raise Exception("Customer user type not found")

        user.user_types.append(customer_type)

        db.session.add(user)
        db.session.commit()

        return user_serializer.jsonify(user), 201
    except IntegrityError:
        return {
            "errors": {"email": ["Email address already exists"]},
            "message": "Email address already exists",
        }, 422
    except ValidationError as e:
        errors = {}
        for field, error_msgs in e.messages.items():
            if field == "password":
                errors[field] = [
                    "Password must be at least 8 characters long and contain at least one uppercase letter, one lowercase letter, one number, and one special character"
                ]
            elif field == "email":
                errors[field] = ["Invalid email format"]
            else:
                errors[field] = error_msgs

        return {"errors": errors, "message": "Validation failed"}, 422


# Login a User
@users_controller.route("/login", methods=["POST"])
def login():
    now_utc = datetime.now(timezone.utc)
    credentials_dictionary = request.json
    user = (
        db.session.query(UserModel)
        .filter_by(email=credentials_dictionary.get("email"))
        .first()
    )
    if not user or not user.validate_password(credentials_dictionary.get("password")):
        return {"message": "Incorrect email or password. Please try again."}, 401

    payload = {"exp": now_utc + timedelta(days=2), "iat": now_utc, "sub": user.id}
    token = jwt.encode(payload, SECRET, algorithm="HS256")
    return {"message": "Login successful", "token": token}


@users_controller.route("/users/<int:user_id>", methods=["PUT"])
@secure_route
def update_user(user_id):
    if g.current_user.id != user_id and not g.current_user.is_admin:
        return {"message": "Unauthorized"}, HTTPStatus.UNAUTHORIZED

    user_data = request.get_json()
    if "newPassword" in user_data and "confirmPassword" in user_data:
        if user_data["newPassword"] != user_data["confirmPassword"]:
            return {"message": "Passwords do not match"}, HTTPStatus.BAD_REQUEST
        if not UserModel.validate_password_format(user_data["newPassword"]):
            return {
                "message": "Password does not meet the required format"
            }, HTTPStatus.BAD_REQUEST
        user_data["password"] = user_data["newPassword"]

    try:
        user = UserModel.query.get_or_404(user_id)
        user = user_serializer.load(user_data, instance=user, partial=True)
        db.session.commit()
        return user_serializer.jsonify(user), HTTPStatus.OK
    except ValidationError as e:
        return {
            "errors": e.messages,
            "message": "Validation failed",
        }, HTTPStatus.BAD_REQUEST


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


# Get current user type
@users_controller.route("/current_user_type", methods=["GET"])
@secure_route
def get_current_user_type():
    if not g.current_user:
        return {"message": "Unauthorized"}, HTTPStatus.UNAUTHORIZED
    return {
        "type": [user_type.name for user_type in g.current_user.user_types]
    }, HTTPStatus.OK
