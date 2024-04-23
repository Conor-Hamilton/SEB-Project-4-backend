from flask import Blueprint, request, jsonify, g
from models.userType import UserType
from serializers.userTypeSchema import UserTypeSchema
from app import db
from marshmallow.exceptions import ValidationError
from http import HTTPStatus
from middleware.secureRoute import secure_route

user_type_controller = Blueprint("user_types", __name__)
user_type_schema = UserTypeSchema()


# Create user types
@user_type_controller.route("/user_types", methods=["POST"])
@secure_route
def create_user_type():
    if not g.current_user.is_admin:
        return {"message": "Unauthorized"}, HTTPStatus.UNAUTHORIZED

    try:
        user_type_data = request.get_json()
        user_type = user_type_schema.load(user_type_data)
        db.session.add(user_type)
        db.session.commit()
        return jsonify(user_type_schema.dump(user_type)), HTTPStatus.CREATED
    except ValidationError as e:
        return {
            "errors": e.messages,
            "message": "Something went wrong",
        }, HTTPStatus.BAD_REQUEST
    except Exception as e:
        return {"message": "Something went wrong"}, HTTPStatus.INTERNAL_SERVER_ERROR


# Get all user types
@user_type_controller.route("/user_types", methods=["GET"])
def get_user_types():
    user_types = UserType.query.all()
    return jsonify(user_type_schema.dump(user_types, many=True)), HTTPStatus.OK


