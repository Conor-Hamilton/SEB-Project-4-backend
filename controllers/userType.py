from flask import Blueprint, request, jsonify
from models.userType import UserType
from serializers.userTypeSchema import UserTypeSchema
from app import db
from marshmallow.exceptions import ValidationError
from http import HTTPStatus

user_type_controller = Blueprint("user_types", __name__)
user_type_schema = UserTypeSchema()

# create user types
@user_type_controller.route("/user_types", methods=["POST"])
def create_user_type():
    try:
        user_type_data = request.get_json()
        user_type = user_type_schema.load(user_type_data)
        db.session.add(user_type)
        db.session.commit()
        return jsonify(user_type_schema.dump(user_type)), 201
    except ValidationError as e:
        return {"errors": e.messages}, HTTPStatus.BAD_REQUEST

# get all user types
@user_type_controller.route("/user_types", methods=["GET"])
def get_user_types():
    user_types = UserType.query.all()
    return jsonify(user_type_schema.dump(user_types, many=True)), 200
